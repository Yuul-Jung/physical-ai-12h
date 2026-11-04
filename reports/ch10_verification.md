# 10차시 기술·적대적 검증 보고서

- 검증일: 2026-11-04
- 차시: 인스턴스 분할과 객체별 마스크 분석
- Markdown A4 인쇄: **11페이지** (Pandoc → HTML → WeasyPrint)
- HTML A4 인쇄: **11페이지** (WeasyPrint)
- 테스트: **18개 통과** (`python -m unittest -v`)
- Python 구문 검사: 2개 파일 통과
- HTML 로컬 상대경로 누락: **0개** (11차시는 예정 링크로 제외)
- 실제 이미지: 합성 데이터로 생성한 scene, instances, mask_01~04.png
- 코드 출력: TP=4, FP=0, FN=0, precision=1.0, recall=1.0
- 검증 범위: 색상 임계값·연결요소 분석으로 분리된 합성 원 4개만 검증. 신경망 학습 또는 실제 도로 이미지 성능을 의미하지 않음.
- 적대적 검토: 접촉 객체 합쳐짐, 조명·색상 변동, 같은 색 배경, 가림, 작은 객체 제거, 픽셀/거리 혼동 위험을 본문에 기술.
- 안전: 로봇 제어 코드 없음. 실제 알티노 AI 제조사 SDK/카메라/라이다/구동: **미검증**.
- 보안: 산출물에 계정·토큰·로컬 사용자 경로를 기입하지 않음. 합성 이미지에 개인정보 없음.
- 공개: GitHub 업로드 수행하지 않음.

## 재현

```bash
python -m pip install numpy opencv-python
cd codes/ch10
python instance_segmentation_lab.py
python -m unittest -v test_instance_segmentation_lab.py
```

## 검증의 한계

실제 알티노 AI 장비의 API·SDK와 모델별 핀/통신 규격은 검증하지 않았다. 합성 영상의 완전 검출은 일반화 성능 지표가 아니다. PDF 페이지 수는 해당 렌더러·폰트·환경 기준이다.
