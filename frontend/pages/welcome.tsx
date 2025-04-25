import React from 'react';
import type { NextPage } from 'next';
import Head from 'next/head';
import { GlobalStyle } from '../components/styles/GlobalStyles';
import WelcomeComponent from '../components/WelcomeComponent';

const Welcome: NextPage = () => {
  return (
    <>
      <Head>
        <title>환영합니다 | 미소녀들의 대화</title>
        <meta name="description" content="로그인 후 환영 페이지" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <GlobalStyle />
      <WelcomeComponent />
    </>
  );
};

export default Welcome; 