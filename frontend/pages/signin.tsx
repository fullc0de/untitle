import React from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import LoginForm from '../components/LoginForm';
import { GlobalStyle } from '../components/styles/GlobalStyles';

const SignIn: NextPage = () => {
  return (
    <>
      <Head>
        <title>로그인 | 미소녀들의 대화</title>
        <meta name="description" content="로그인 페이지" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <GlobalStyle />
      <LoginForm />
    </>
  );
};

export default SignIn; 