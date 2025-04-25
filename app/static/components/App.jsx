import React from 'react';
import RoundedButton from './RoundedButton';
import styled from 'styled-components';
import { BaseContainer, Container, Title } from './styles/GlobalStyles';

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: row;
  gap: 30px;
  margin: 20px 20px;
  justify-content: center;
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 10px;
    align-items: center;
  }
`;

const App = () => {
  return (
    <BaseContainer>
      <Container>
      <Title>미소녀들의 대화</Title>
      <ButtonContainer>
        <RoundedButton variant="success" onClick={() => window.location.href = '/signup'}>
          가입하기
        </RoundedButton>
        <RoundedButton variant="primary" onClick={() => window.location.href = '/signin'}>
          로그인하기
        </RoundedButton>
      </ButtonContainer>
      </Container>
    </BaseContainer>
  );
};

export default App; 