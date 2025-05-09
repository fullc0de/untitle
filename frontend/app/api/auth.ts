import { apiConfig } from '../config/api';

interface SignUpResponse {
  id: number;
  username: string;
  token: string;
}

interface SignInResponse {
  id: number;
  username: string;
  token: string;
}

export const signUp = async (
  username: string,
  password: string
): Promise<SignUpResponse> => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const response = await fetch(`${apiConfig.baseURL}/api/signup`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('회원가입에 실패했습니다.');
  }

  return response.json();
};

export const signIn = async (
  username: string,
  password: string
): Promise<SignInResponse> => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const response = await fetch(`${apiConfig.baseURL}/api/signin`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('로그인에 실패했습니다.');
  }

  return response.json();
};

export const getCurrentUser = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('인증되지 않은 사용자입니다.');
  }

  const response = await fetch(`${apiConfig.baseURL}/api/user/me`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('사용자 정보를 가져오는데 실패했습니다.');
  }

  return response.json();
}; 