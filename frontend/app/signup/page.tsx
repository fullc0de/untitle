'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { signUp } from '../api/auth';

export default function SignUp() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await signUp(username, password);
      localStorage.setItem('token', response.token);
      router.push('/');
    } catch (error) {
      setError(error instanceof Error ? error.message : '회원가입에 실패했습니다.');
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="card w-96 bg-base-100 shadow-xl">
        <div className="card-body">
          <h1 className="card-title text-2xl font-bold mb-4">회원가입</h1>
          {error && (
            <div className="alert alert-error mb-4">
              <span>{error}</span>
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="form-control">
              <label className="label">
                <span className="label-text">사용자 이름</span>
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input input-bordered"
                required
              />
            </div>
            <div className="form-control">
              <label className="label">
                <span className="label-text">비밀번호</span>
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input input-bordered"
                required
              />
            </div>
            <div className="form-control mt-6">
              <button type="submit" className="btn btn-primary">
                가입하기
              </button>
            </div>
          </form>
          <div className="text-center mt-4">
            <Link href="/signin" className="link link-primary">
              이미 계정이 있으신가요? 로그인
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
} 