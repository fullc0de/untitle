import React, { useState } from 'react';
import { Container, Title, Button, FormGroup, ErrorMessage } from './styles/GlobalStyles';

const LoginForm: React.FC = () => {
  const [error, setError] = useState<boolean>(false);

  return (
    <Container>
      <Title>로그인</Title>
      <FormGroup>
        <label htmlFor="email">이메일</label>
        <input type="email" id="email" />
      </FormGroup>
      <FormGroup>
        <label htmlFor="password">비밀번호</label>
        <input type="password" id="password" />
      </FormGroup>
      <Button>로그인</Button>
      <ErrorMessage $show={error}>로그인에 실패했습니다.</ErrorMessage>
    </Container>
  );
};

export default LoginForm; 