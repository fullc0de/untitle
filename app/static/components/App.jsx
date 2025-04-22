import React from 'react';
import RoundedButton from './RoundedButton';

const App = () => {
  return (
    <div className="container">
      <h1>미소녀들의 대화</h1>
      <div className="button-container">
        <RoundedButton variant="success" onClick={() => window.location.href = '/signup'}>
          가입하기
        </RoundedButton>
        <RoundedButton variant="primary" onClick={() => window.location.href = '/signin'}>
          로그인하기
        </RoundedButton>
      </div>
    </div>
  );
};

export default App; 