"""10차시 선택 심화: PyTorch 1×1 Conv 픽셀 분류 학습 + 연결영역 인스턴스 분리.
완전한 Mask R-CNN이 아닌 교육용 합성 데이터에서의 하이브리드 실습.
"""
from pathlib import Path
import json
import cv2
import numpy as np
import torch
from torch import nn

PALETTE = {1:(0,0,220), 2:(0,180,0), 3:(220,0,0)}


class PixelClassifier(nn.Module):
    """3채널 BGR에서 배경·빨강·초록·파랑 픽셀 로짓을 학습한다."""
    def __init__(self):
        super().__init__()
        self.layer = nn.Conv2d(3, 4, kernel_size=1)

    def forward(self, x):
        return self.layer(x)


def make_dataset(seed=17, count=24, height=48, width=64):
    """위치만 달라지는 합성 학습/검증 이미지 및 픽셀 정답 마스크."""
    rng=np.random.default_rng(seed)
    inputs, labels=[], []
    for _ in range(count):
        image = np.full((height,width,3), (235,235,235), dtype=np.uint8)
        truth = np.zeros((height,width), dtype='uint8')
        for cls, pos in ((1,12),(2,31),(3,49)):
            dx=int(rng.integers(-3,4)); dy=int(rng.integers(-7,8))
            center=(pos+dx,24+dy)
            cv2.circle(image, center, 6, PALETTE[cls], -1)
            cv2.circle(truth, center, 6, cls, -1)
        inputs.append(image.transpose(2,0,1).astype('float32')/255.0)
        labels.append(truth.astype('int64'))
    return torch.tensor(np.stack(inputs)), torch.tensor(np.stack(labels))


def train_model(epochs=140):
    torch.manual_seed(53)
    model=PixelClassifier()
    optimizer=torch.optim.Adam(model.parameters(), lr=0.06)
    x,y=make_dataset(seed=17)
    for _ in range(epochs):
        optimizer.zero_grad()
        logits=model(x)
        loss=nn.functional.cross_entropy(logits,y, weight=torch.tensor([0.5,3.,3.,3.]))
        loss.backward()
        optimizer.step()
    model.eval()
    vx,vy=make_dataset(seed=223,count=6)
    with torch.no_grad():
        predicted=model(vx).argmax(dim=1)
    acc=float((predicted==vy).float().mean())
    return model, acc


def instance_masks(model, image_bgr, min_area=25):
    """모델이 분류한 동일 클래스 픽셀을 연결영역으로 다시 나누기."""
    if image_bgr.ndim != 3 or image_bgr.shape[2] != 3:
        raise ValueError('H×W×3 BGR 이미지가 필요합니다')
    input_tensor=torch.tensor(image_bgr.transpose(2,0,1).copy(),dtype=torch.float32)[None]/255.0
    with torch.no_grad():
        category=model(input_tensor).argmax(1).squeeze(0).numpy().astype('uint8')
    found=[]
    for cls in (1,2,3):
        binary=(category==cls).astype('uint8')
        n,ids,stats,_=cv2.connectedComponentsWithStats(binary,8)
        for i in range(1,n):
            x,y,w,h,area=map(int,stats[i])
            if area>=min_area:
                found.append({'class_index':cls,'box':[x,y,x+w,y+h], 'area':area})
    return category, found


def run_demo():
    model, accuracy=train_model()
    x,_=make_dataset(seed=223,count=1)
    frame=(x[0].numpy().transpose(1,2,0)*255).round().astype('uint8')
    mask, instances=instance_masks(model,frame)
    out=Path(__file__).parent/'outputs';out.mkdir(parents=True,exist_ok=True)
    cv2.imwrite(str(out/'learned_scene.png'),frame)
    cv2.imwrite(str(out/'learned_mask.png'),mask*70)
    data={'held_out_pixel_accuracy': accuracy,'instances':instances}
    (out/'learned_results.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print('독립 합성 장면 픽셀 정확도:',f'{accuracy:.1%}','객체 수:',len(instances))
    return data


if __name__=='__main__':run_demo()
