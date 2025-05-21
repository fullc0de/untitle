'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { getCurrentUser } from '../api/auth';

interface HeaderProps {
  title?: string;
  showBackButton?: boolean;
  backUrl?: string;
}

export default function Header({ title, showBackButton = false, backUrl = '/chatrooms' }: HeaderProps) {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        await getCurrentUser();
        setIsAuthenticated(true);
      } catch (error) {
        setIsAuthenticated(false);
        router.push('/');
      }
    };

    checkAuth();
  }, [router]);

  if (!isAuthenticated) {
    return null;
  }

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    router.push('/');
  };

  return (
    <div className="sticky top-0 z-10 border-b border-sn-border bg-sn-text-dark shadow-sn-sm flex flex-col">
      <div className="flex flex-row relative h-14">
        {/* 좌측 영역 */}
        <div className="flex-1 flex items-center">
          {showBackButton && (
            <Link href={backUrl} className="btn btn-ghost text-sn-text-light hover:bg-sn-hover">
              ← 목록으로
            </Link>
          )}
        </div>

        {/* 중앙 타이틀 영역 - 절대 위치로 배치 */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <h1 className="text-xl font-semibold text-sn-text-light">
            {title || '채팅방'}
          </h1>
        </div>

        {/* 우측 영역 */}
        <div className="flex-1 flex items-center justify-end px-4">
          <button onClick={handleLogout} className="btn btn-ghost text-sn-text-light hover:bg-sn-hover">
            로그아웃
          </button>
        </div>
      </div>
    </div>
  );
} 