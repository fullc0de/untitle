import React from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import { GlobalStyle } from '../components/styles/GlobalStyles';
import { BaseContainer, Container, Title, FormGroup, Button, ErrorMessage } from '../components/styles/GlobalStyles';
import { useState } from 'react';

const SignUp: NextPage = () => {
  const [error, setError] = useState<boolean>(false);

  return (
    <>
      <Head>
        <title>가입하기 | 미소녀들의 대화</title>
        <meta name="description" content="회원가입 페이지" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <GlobalStyle />
      <BaseContainer>
        <Container>
          <Title>회원가입</Title>
          <FormGroup>
            <label htmlFor="email">이메일</label>
            <input type="email" id="email" />
          </FormGroup>
          <FormGroup>
            <label htmlFor="password">비밀번호</label>
            <input type="password" id="password" />
          </FormGroup>
          <FormGroup>
            <label htmlFor="confirmPassword">비밀번호 확인</label>
            <input type="password" id="confirmPassword" />
          </FormGroup>
          <Button>가입하기</Button>
          <ErrorMessage $show={error}>회원가입에 실패했습니다.</ErrorMessage>
        </Container>
      </BaseContainer>
    </>
  );
};

export default SignUp; 