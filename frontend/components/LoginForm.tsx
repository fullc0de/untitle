import React, { useState } from 'react';
import { Container, Title, Button, FormGroup, ErrorMessage } from './styles/GlobalStyles';
import { useRouter } from 'next/router';

const LoginForm: React.FC = () => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('로그인에 실패했습니다.');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(false);

    try {
      const response = await fetch('http://localhost:8000/api/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          username: username,
          password: password 
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || '로그인에 실패했습니다.');
        setError(true);
        return;
      }

      const data = await response.json();
      
      // 토큰과 사용자 정보를 로컬 스토리지에 저장
      localStorage.setItem('token', data.token);
      localStorage.setItem('userId', data.id.toString());
      localStorage.setItem('username', data.username);
      
      // 로그인 성공 시 환영 페이지로 이동
      router.push('/welcome');
    } catch (err) {
      console.error('로그인 에러:', err);
      setErrorMessage('서버 연결에 문제가 발생했습니다.');
      setError(true);
    }
  };

  return (
    <Container>
      <Title>로그인</Title>
      <form onSubmit={handleLogin}>
        <FormGroup>
          <label htmlFor="username">사용자 이름</label>
          <input 
            type="text" 
            id="username" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </FormGroup>
        <FormGroup>
          <label htmlFor="password">비밀번호</label>
          <input 
            type="password" 
            id="password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </FormGroup>
        <Button type="submit">로그인</Button>
        <ErrorMessage $show={error}>{errorMessage}</ErrorMessage>
      </form>
    </Container>
  );
};

export default LoginForm; 