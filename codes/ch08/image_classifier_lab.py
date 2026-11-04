"""08차시: 외부 데이터 없이 합성 도형 3종을 학습하는 이미지 분류."""
from pathlib import Path
import argparse, json, random
import numpy as np
import torch
from torch import nn
from PIL import Image, ImageDraw

LABELS = ('circle', 'square', 'triangle')

def make_image(label, seed, size=32):
    """각 클래스의 위치·크기·밝기를 달리한 RGB 합성 이미지를 생성한다."""
    rng = random.Random(seed)
    im = Image.new('RGB', (size, size), (18, 23, 31))
    draw = ImageDraw.Draw(im)
    offset_x, offset_y = rng.randint(-3, 3), rng.randint(-3, 3)
    half = rng.randint(7, 10)
    cx, cy = size//2+offset_x, size//2+offset_y
    color = (rng.randint(170,255), rng.randint(160,245), rng.randint(150,235))
    if label == 0:
        draw.ellipse((cx-half, cy-half, cx+half, cy+half), fill=color)
    elif label == 1:
        draw.rectangle((cx-half, cy-half, cx+half, cy+half), fill=color)
    elif label == 2:
        draw.polygon([(cx,cy-half),(cx-half,cy+half),(cx+half,cy+half)],fill=color)
    else:
        raise ValueError('label must be 0, 1 or 2')
    return im

def dataset(n_per_class=40, seed=2026):
    """학습/평가를 분리하기 전에 서로 다른 시드로 표본을 만든다."""
    images, labels = [], []
    for cls in range(3):
        for i in range(n_per_class):
            im = make_image(cls, seed+cls*10000+i)
            a = np.asarray(im, dtype=np.float32) / 255.0
            images.append(np.transpose(a, (2,0,1)))
            labels.append(cls)
    return torch.tensor(np.stack(images)), torch.tensor(labels, dtype=torch.long)

class TinyCNN(nn.Module):
    """3x32x32 → 특징맵 → 3개 클래스 점수(logits)."""
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(nn.Conv2d(3,8,3,padding=1),nn.ReLU(),
            nn.MaxPool2d(2),nn.Conv2d(8,16,3,padding=1),nn.ReLU(),
            nn.AdaptiveAvgPool2d((4,4)))
        self.classifier = nn.Linear(16*4*4, 3)
    def forward(self,x):
        return self.classifier(torch.flatten(self.features(x),1))

def split_indices(labels, train_ratio=0.8, seed=77):
    """각 클래스별 80:20 분리. 동일 원본의 증강본이 양쪽에 들어가지 않도록 설계."""
    g=torch.Generator().manual_seed(seed)
    train, test=[],[]
    for c in range(3):
        ids=torch.where(labels==c)[0]
        ids=ids[torch.randperm(len(ids),generator=g)].tolist()
        cut=int(len(ids)*train_ratio)
        train.extend(ids[:cut]); test.extend(ids[cut:])
    return train,test

def confusion_matrix(y_true,y_pred,n=3):
    """행은 실제 클래스, 열은 예측 클래스."""
    m=np.zeros((n,n),dtype=int)
    for t,p in zip(y_true,y_pred): m[int(t),int(p)]+=1
    return m

def train_demo(out_dir, epochs=50, n_per_class=40):
    torch.manual_seed(42); np.random.seed(42)
    torch.set_num_threads(1)
    x,y=dataset(n_per_class=n_per_class)
    tr,te=split_indices(y)
    model=TinyCNN(); optimizer=torch.optim.Adam(model.parameters(),lr=0.006)
    loss_fn=nn.CrossEntropyLoss()
    for epoch in range(epochs):
        model.train(); optimizer.zero_grad()
        loss=loss_fn(model(x[tr]),y[tr]);loss.backward();optimizer.step()
        print(f'epoch {epoch+1:02d} loss={loss.item():.4f}')
    model.eval()
    with torch.no_grad():
        logits=model(x[te]);pred=logits.argmax(1)
        acc=(pred==y[te]).float().mean().item()
        cm=confusion_matrix(y[te].tolist(),pred.tolist())
        probs=torch.softmax(logits,dim=1)
    out=Path(out_dir);out.mkdir(parents=True,exist_ok=True)
    torch.save(model.state_dict(),out/'tinycnn_weights.pt')
    Image.fromarray((x[0].permute(1,2,0).numpy()*255).astype('uint8')).resize((256,256)).save(out/'sample_circle.png')
    report={'classes':list(LABELS),'train_count':len(tr),'test_count':len(te),
        'accuracy':round(acc,4),'confusion_matrix':cm.tolist(),
        'first_prediction':LABELS[int(pred[0])],
        'first_confidence':round(float(probs[0].max()),4),
        'note':'합성 도형 평가 정확도이며 실제 도로 객체 성능이 아님'}
    (out/'metrics.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='outputs/ch08')
    parser.add_argument('--epochs',type=int,default=50)
    args=parser.parse_args()
    train_demo(args.out,epochs=args.epochs)
