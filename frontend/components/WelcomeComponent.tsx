import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import styled from 'styled-components';
import { BaseContainer, Container, Title, Button } from './styles/GlobalStyles';

const LogoutButton = styled(Button)`
  background-color: #f44336;
  color: white;
  margin: 0 auto;
  display: block;
  
  &:hover {
    background-color: #d32f2f;
  }
`;

const WelcomeContainer = styled(Container)`
  text-align: center;
`;

const WelcomeComponent: React.FC = () => {
  const [username, setUsername] = useState<string>('');
  const router = useRouter();

  useEffect(() => {
    // 클라이언트 측에서만 실행되도록
    if (typeof window !== 'undefined') {
      const storedUsername = localStorage.getItem('username');
      const token = localStorage.getItem('token');
      
      if (!token) {
        // 로그인되지 않은 사용자는 로그인 페이지로 리디렉션
        router.push('/signin');
        return;
      }
      
      setUsername(storedUsername || '사용자');
    }
  }, [router]);

  const handleLogout = () => {
    // 로컬 스토리지에서 사용자 정보 삭제
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    
    // 로그아웃 후 홈 페이지로 이동
    router.push('/');
  };

  return (
    <BaseContainer>
      <WelcomeContainer>
        <Title>안녕하세요, {username}</Title>
        <LogoutButton onClick={handleLogout}>로그아웃</LogoutButton>
      </WelcomeContainer>
    </BaseContainer>
  );
};

export default WelcomeComponent; 