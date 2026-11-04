# 자율주행 자동차 로봇을 활용한 피지컬 AI — 12시간 교육자료

## 1. 내용과 사용 범위

- 기준: 교육과정 안내서의 12차시(1일차 6시간 + 2일차 6시간). 원본 PDF는 공개 저장소에 포함하지 않는다.
- 각 차시: Markdown + HTML + Python 예제 + 자동 테스트. HTML 시작점: `index.html`
- 기본 60분 실습과 선택 심화를 구분. 09·10차시 선택 심화에는 학습형 하이브리드 모델 추가.
- **실제 알티노 AI SDK·센서·제어 및 주행 검증은 수행하지 않았다.** PC/CPU 합성 데이터와 모의 판단 중심.
- 개인정보가 포함된 실장비 화면 캡처는 포함하지 않았다. 실제 장비 접근 및 제조사 SDK 검증 전까지 실제 주행 실습을 수행하지 않는다.

## 2. 환경 설치 (PC/Ubuntu)

```bash
python3 -m venv .venv                   # 독립 Python 가상환경 생성
source .venv/bin/activate              # 현재 셸에서 가상환경 활성화
python -m pip install -r requirements.txt  # 실습에 필요한 라이브러리 설치
```

Python 3.10 이상을 권장한다. 설치 후 `python -c "import numpy, cv2, torch; print('READY')"`로 패키지를 확인한다. Ubuntu의 특정 장비나 Jetson에 일반 PC용 PyTorch 패키지를 무조건 덮어쓰지 않는다. Jetson에는 보드에 설치된 JetPack·Python·CUDA와 호환되는 NVIDIA 배포 방법을 먼저 확인한다.

## 3. 실행 및 검증

```bash
python codes/ch01/system_probe.py
python codes/ch02/steering_sim.py
python codes/ch04/robot_python_lab.py
python codes/ch09/object_detection_lab.py
python codes/ch09/hybrid_learned_detector.py       # 선택 심화·학습형 후보 분류
python codes/ch10/learned_pixel_segmentation.py   # 선택 심화·학습형 픽셀 분류
```

모든 테스트(각 차시 독립 실행):

```bash
for n in $(seq -w 1 12); do
  python -m unittest discover -s "codes/ch${n}" -p 'test_*.py' -v
done
```

모든 명령은 이 저장소의 최상위 폴더(`requirements.txt`와 `index.html`이 있는 위치)에서 실행한다. 본문이나 코드를 내려받아 사용할 때는 ZIP을 전체 압축 해제하여 HTML·SVG·PNG·CSS의 상대경로를 보존한다.

## 4. 검증·출처·제약

- 차시별 원래 검증 로그: `reports/chXX_verification.md` (역사적 보고서, 이번 감사 이전 작성)
- 전수 감사·보완 사항: `reports/ADVERSARIAL_AUDIT.md` (최신 우선)
- A4 인쇄 페이지 수·자동 테스트 실측: `reports/validation_results.json`
- `manifest.json`: 보존된 파일과 미검증 범위의 단일 통합 상태
- 단순 규칙 기반 09·10차시 기본 실습을 전체 딥러닝 모델 훈련 성과로 해석하지 않는다. 선택 심화는 AI 학습 요소를 보강했지만 Mask R-CNN/YOLO를 실물에 적용한 것은 아니다.

## 5. 출처

- 사용자 제공 `과정 안내서(1).pdf`, 1~2쪽
- Python 공식: https://docs.python.org/3/tutorial/
- NumPy 공식: https://numpy.org/doc/stable/
- OpenCV 공식: https://docs.opencv.org/4.x/
- PyTorch 객체 검출·분할 공식: https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html
- NVIDIA Jetson 개발자 문서: https://developer.nvidia.com/embedded/learn/getting-started-jetson

## 6. 공개 저장소 안내

- 웹 교재 시작: [`index.html`](index.html)
- GitHub Pages: Settings → Pages → Deploy from a branch → `main` / `(root)` 선택
- 외부 서비스 계정·개인 문서·실제 장비 로그는 공개 저장소에 업로드하지 않는다.
- 본 자료는 교육용 코드 및 합성 데이터 검증본이며 실물 자율주행 안전성 인증 자료가 아니다.
