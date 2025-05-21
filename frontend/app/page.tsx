'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { getCurrentUser } from './api/auth';

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        await getCurrentUser();
        setIsAuthenticated(true);
        router.push('/chatroom');
      } catch (error) {
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  if (isLoading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center bg-sn-bg">
        <div className="loading loading-spinner loading-lg text-sn-primary"></div>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-sn-bg">
      <div className="card w-96 bg-sn-text-dark shadow-sn rounded-sn border border-sn-border">
        <div className="card-body items-center text-center">
          <h1 className="card-title text-4xl font-bold mb-8 text-sn-text-light">환영합니다</h1>
          <div className="flex gap-4">
            <Link 
              href="/signup" 
              className="btn bg-sn-primary hover:bg-sn-primary-600 text-sn-text-light shadow-sn-button rounded-sn-sm"
            >
              Sign Up
            </Link>
            <Link 
              href="/signin" 
              className="btn bg-sn-secondary hover:bg-sn-secondary-600 text-sn-text-dark shadow-sn-sm rounded-sn-sm"
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
} 