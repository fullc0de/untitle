'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { io } from 'socket.io-client';
import { getCurrentUser } from './api/auth';
import { createChatroom, getChatrooms, getChats, sendChat, Chat } from './api/chat';

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [messages, setMessages] = useState<Chat[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [chatroomId, setChatroomId] = useState<number | null>(null);
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        await getCurrentUser();
        setIsAuthenticated(true);
        initializeChatroom();
      } catch (error) {
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  // 웹소켓 연결 설정
  useEffect(() => {
    if (!isAuthenticated || !chatroomId) return;

    const socket = io(process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'ws://localhost:8000', {
      path: '/socket.io',
      transports: ['websocket'],
    });

    socket.on('connect', () => {
      console.log('웹소켓 연결됨');
    });

    socket.on('message', (data) => {
      console.log('수신된 데이터:', data);
      // // data가 이미 JSON 객체인 경우 파싱하지 않음
      // const chatData = typeof data.data === 'string' ? JSON.parse(data.data) : data.data;
      // console.log('파싱된 메시지:', chatData);
      setMessages(prevMessages => [...prevMessages, data]);
    });

    socket.on('disconnect', () => {
      console.log('웹소켓 연결 해제됨');
    });

    return () => {
      socket.disconnect();
    };
  }, [isAuthenticated, chatroomId]);

  const initializeChatroom = async () => {
    try {
      // 기존 채팅방 목록 조회
      const chatrooms = await getChatrooms();
      
      if (chatrooms.length > 0) {
        // 가장 최근에 생성된 채팅방 선택
        const latestChatroom = chatrooms.reduce((latest, current) => {
          return new Date(current.created_at) > new Date(latest.created_at)
            ? current
            : latest;
        });
        
        setChatroomId(latestChatroom.id);
        loadMessages(latestChatroom.id);
      } else {
        // 채팅방이 없는 경우 새로 생성
        const chatroom = await createChatroom();
        setChatroomId(chatroom.id);
        loadMessages(chatroom.id);
      }
    } catch (error) {
      setError('채팅방 초기화에 실패했습니다.');
    }
  };

  const loadMessages = async (roomId: number) => {
    try {
      const chats = await getChats(roomId);
      setMessages(chats);
    } catch (error) {
      setError('메시지를 불러오는데 실패했습니다.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    router.push('/');
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim() || !chatroomId) return;

    try {
      const chat = await sendChat(chatroomId, newMessage);
      setMessages([...messages, chat]);
      setNewMessage('');
    } catch (error) {
      setError('메시지 전송에 실패했습니다.');
    }
  };

  if (!isAuthenticated) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24">
        <div className="card w-96 bg-base-100 shadow-xl">
          <div className="card-body items-center text-center">
            <h1 className="card-title text-4xl font-bold mb-8">환영합니다</h1>
            <div className="flex gap-4">
              <Link href="/signup" className="btn btn-primary">
                Sign Up
              </Link>
              <Link href="/signin" className="btn btn-secondary">
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col">
      <div className="flex justify-end p-4">
        <button onClick={handleLogout} className="btn btn-ghost">
          로그아웃
        </button>
      </div>

      {error && (
        <div className="alert alert-error mx-4">
          <span>{error}</span>
        </div>
      )}
      
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full p-4">
        <div className="flex-1 overflow-y-auto mb-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender_type === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-[70%] p-4 rounded-lg ${
                  message.sender_type === 'user'
                    ? 'bg-primary text-primary-content'
                    : 'bg-base-200'
                }`}
              >
                {message.content.text}
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            className="input input-bordered flex-1"
            placeholder="메시지를 입력하세요..."
          />
          <button type="submit" className="btn btn-primary">
            전송
          </button>
        </form>
      </div>
    </main>
  );
} 