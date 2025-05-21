'use client';

import { useEffect, useState } from 'react';
import { createChatroom } from '../../api/chat';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Header from '../../components/Header';

export default function NewChatroomPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const createNewChatroom = async () => {
      setLoading(true);
      try {
        const newChatroom = await createChatroom();
        router.push(`/chatrooms/${newChatroom.id}`);
      } catch (err) {
        setError(err instanceof Error ? err.message : '채팅방 생성에 실패했습니다.');
      } finally {
        setLoading(false);
      }
    };

    createNewChatroom();
  }, [router]);

  if (loading) {
    return (
      <div className="flex flex-col min-h-screen">
        <Header title="새 채팅방 생성" showBackButton={true} />
        <div className="flex-1 flex justify-center items-center">
          <span className="loading loading-spinner loading-lg"></span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col min-h-screen">
        <Header title="새 채팅방 생성" showBackButton={true} />
        <div className="flex-1 flex flex-col items-center justify-center gap-4">
          <div className="alert alert-error">
            <span>{error}</span>
          </div>
          <Link href="/chatrooms" className="btn btn-primary">
            목록으로 돌아가기
          </Link>
        </div>
      </div>
    );
  }

  return null;
} 