# GitHub Pages 게시 절차

- 새 저장소: `Yuul-Jung/physical-ai-12h` (공개 여부는 사용자가 확인)
- 압축을 풀어 이 폴더의 **내용물**(`index.html`, `chapters/`, `codes/`, `assets/`, `reports/` 등)을 저장소 최상위에 올린다.
- GitHub 저장소 → Settings → Pages → Build and deployment → Source에서 `GitHub Actions`를 최초 1회 선택한다.
- `.github/workflows/deploy-pages.yml`이 `main` 변경 때 사이트를 자동 게시한다. 최초 Pages 설정은 저장소 관리자가 수행해야 한다.
- 사이트가 활성화된 뒤 `index.html`과 12개 `chapters/chXX.html` 파일이 보이는지 확인한다.
- 공식 SDK와 실물 카메라·라이다·모터·비상정지 기능은 아직 검증되지 않았다.
- PDF 원본·개인정보·인증정보·로컬 폴더 화면 캡처는 포함하지 않는다.
- 본 교재의 외부 참고자료 링크와 라이선스는 원저작자 정책을 따른다. 별도의 재배포 라이선스는 부여하지 않았다.
