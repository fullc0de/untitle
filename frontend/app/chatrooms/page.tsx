'use client';

import { useEffect, useState } from 'react';
import { Chatroom } from '../api/chat';
import { getChatrooms, createChatroom } from '../api/chat';
import Link from 'next/link';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import Header from '../components/Header';

export default function ChatroomsPage() {
  const [chatrooms, setChatrooms] = useState<Chatroom[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    const fetchChatrooms = async () => {
      try {
        const data = await getChatrooms();
        setChatrooms(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : '채팅방을 불러오는데 실패했습니다.');
      } finally {
        setLoading(false);
      }
    };

    fetchChatrooms();
  }, []);

  const handleCreateChatroom = async () => {
    try {
      setIsCreating(true);
      // TODO: 채팅방 생성 API 호출
      const newChatroom = await createChatroom(); // API 호출 결과
      setChatrooms(prev => [newChatroom, ...prev]);
    } catch (err) {
      setError(err instanceof Error ? err.message : '채팅방 생성에 실패했습니다.');
    } finally {
      setIsCreating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-500 border-r-4 border-transparent"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="alert alert-error">
          <span>{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-sn-bg">
      <Header title="채팅방 목록" />
      <div className="container mx-auto p-4 flex-1">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {chatrooms.map((chatroom) => (
            <Link href={`/chatrooms/${chatroom.id}`} key={chatroom.id}>
              <div 
                className="card h-48 cursor-pointer hover:shadow-lg transition-shadow bg-sn-bg-room-card"
                style={{ borderColor: chatroom.property?.latest_emotion_color || '#ffffff', borderWidth: '4px' }}
              >
                <div className="card-body flex flex-col justify-between gap-4">
                  <div className="flex-1 flex items-center justify-center flex-col gap-2">
                    {chatroom.property?.bot_name && (
                      <div className="text-lg text-center font-[500] text-gray-100">
                        {chatroom.property.bot_name}
                      </div>
                    )}
                    <div className="text-xl font-semibold text-center text-gray-100">
                      {chatroom.property?.latest_emotion_text || '새로운 대화'}
                    </div>
                    {chatroom.property?.latest_message && (
                      <div className="text-sm text-center line-clamp-2 text-gray-200">
                        {chatroom.property.latest_message}
                      </div>
                    )}
                  </div>
                  <div className="text-right text-sm text-gray-600">
                    {format(new Date(chatroom.updated_at), 'yyyy년 MM월 dd일 HH:mm', { locale: ko })}
                  </div>
                </div>
              </div>
            </Link>
          ))}
          
          {/* 새 채팅방 생성 카드 */}
          <div 
            className="card h-48 cursor-pointer hover:shadow-lg transition-shadow bg-sn-bg-room-card"
            onClick={handleCreateChatroom}
          >
            <div className="card-body flex flex-col items-center justify-center">
              {isCreating ? (
                <span className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-500 border-r-4 border-transparent"></span>
              ) : (
                <>
                  <div className="text-6xl mb-2 text-sn-text-light">+</div>
                  <div className="text-lg font-bold text-sn-text-mid">추가하기</div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 