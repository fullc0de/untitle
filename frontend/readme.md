




# 프로젝트 설정과 관련한 히스토리
## Next.js와 styled-components 하이드레이션 문제 해결 방법

### 문제
Next.js와 styled-components를 함께 사용할 때 다음과 같은 하이드레이션 오류가 발생할 수 있습니다:
`Warning: Prop 'className' did not match. Server: "sc-guGTOK XXsvU" Client: "sc-dKREkF dKLJmI"`

### 해결 방법

1. **_document.tsx 파일 생성**
   - `ServerStyleSheet` 클래스를 사용하여 서버 사이드 렌더링 설정
   - 서버와 클라이언트 간 일관된 클래스명 생성을 위한 초기 스타일 수집

2. **Next.js 컴파일러 설정 추가**
   ```js
   // next.config.js
   compiler: {
     styledComponents: true,
   }
   ```

3. **Node.js 최신 버전 사용**
   - `nvm use 20` 또는 그 이상 버전 사용 권장

위 설정을 적용하면 클라이언트와 서버 간 스타일 불일치로 인한 하이드레이션 오류를 해결할 수 있습니다.
