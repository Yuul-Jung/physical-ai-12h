# 08차시 기술·적대적 검증 보고서

- 검증일: 2026-11-04
- 교육범위: 이미지 분류·합성 이미지·CNN·평가 지표·안전 한계
- Markdown A4 인쇄: 13페이지 (Pandoc HTML 변환 후 WeasyPrint 기준)
- HTML A4 인쇄: 10페이지 (WeasyPrint 기준)
- Python unittest: 11개 통과
- 실제 학습: CPU PyTorch 50 epoch 실행
- 훈련/평가: 96/24개, 클래스별 평가 8개
- 평가 정확도: 0.875 (21/24), 합성 데이터 한정
- 혼동행렬: [[7,0,1],[1,7,0],[1,0,7]]
- 출력: metrics.json, tinycnn_weights.pt, sample_circle.png
- 점검: 훈련/평가 분리, shape, 값 범위, 클래스 범위, 출력 파일, 공개 보안, 합성 데이터 한계
- 미검증: 알티노 AI SDK·카메라·Jetson GPU·실제 주행 및 실환경 인식
- 참고 문서: PyTorch CrossEntropyLoss/Conv2d/state_dict, NumPy transpose, Pillow ImageDraw, Python unittest
- 적대적 검증 한계: 공식 문서 실시간 접근 여부와 실제 하드웨어 재현은 확인하지 못함.
- 판단: 교육용 CPU 합성 데이터 실습 PASS, 하드웨어 연동 UNVERIFIED.
