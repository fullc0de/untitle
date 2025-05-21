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
      router.push('/chatrooms');
    } catch (error) {
      setError(error instanceof Error ? error.message : '회원가입에 실패했습니다.');
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-sn-bg">
      <div className="card w-96 bg-sn-text-dark shadow-sn rounded-sn border border-sn-border">
        <div className="card-body">
          <h1 className="card-title text-2xl font-bold mb-4 text-sn-text-light">회원가입</h1>
          {error && (
            <div className="alert alert-error mb-4 bg-sn-accent-900 text-sn-text-light border-sn-accent">
              <span>{error}</span>
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="form-control">
              <label className="label">
                <span className="label-text text-sn-text-mid">사용자 이름</span>
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input input-bordered bg-sn-text-dark border-sn-border text-sn-text-light"
                required
              />
            </div>
            <div className="form-control">
              <label className="label">
                <span className="label-text text-sn-text-mid">비밀번호</span>
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input input-bordered bg-sn-text-dark border-sn-border text-sn-text-light"
                required
              />
            </div>
            <div className="form-control mt-6">
              <button type="submit" className="btn bg-sn-primary hover:bg-sn-primary-600 text-sn-text-light shadow-sn-button rounded-sn-sm">
                가입하기
              </button>
            </div>
          </form>
          <div className="text-center mt-4">
            <Link href="/signin" className="link text-sn-primary hover:text-sn-primary-400">
              이미 계정이 있으신가요? 로그인
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
} 