'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { io } from 'socket.io-client';
import { getCurrentUser } from '../api/auth';
import { createChatroom, getChatrooms, getChats, sendChat, Chat } from '../api/chat';

export default function ChatRoom() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [messages, setMessages] = useState<Chat[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [chatroomId, setChatroomId] = useState<number | null>(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [showNewMessageToast, setShowNewMessageToast] = useState(false);
  const [latestMessage, setLatestMessage] = useState<Chat | null>(null);
  const [headerColor, setHeaderColor] = useState('hsl(var(--b1))');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [isInitialLoad, setIsInitialLoad] = useState(true);
  const [isWaitingForBotMessage, setIsWaitingForBotMessage] = useState(false);
  const [autoScrollEnabled, setAutoScrollEnabled] = useState(true);
  
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        await getCurrentUser();
        setIsAuthenticated(true);
        initializeChatroom();
      } catch (error) {
        setIsAuthenticated(false);
        router.push('/signin');
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

    socket.on('message', (data: Chat) => {
      console.log('수신된 데이터:', data);
      setIsWaitingForBotMessage(false);
      // 현재 스크롤 위치 확인
      const isCurrentlyNearBottom = checkIfNearBottom();
            
      // 스크롤 위치에 따른 처리
      if (!isCurrentlyNearBottom) {
        console.log('화면 하단과 멀리 있음, 토스트 표시');
        setShowNewMessageToast(true);
        setLatestMessage(data);
        setAutoScrollEnabled(false);
        
        // 8초 후 토스트 메시지 자동으로 닫기
        console.log('8초 후 토스트 메시지 자동으로 닫기:', new Date().toLocaleString());
        setTimeout(() => {
          console.log('Fire!', new Date().toLocaleString());
          setShowNewMessageToast(false);
        }, 8000);
      } else {
        // 하단 가까이 있으면 자동 스크롤 활성화
        setAutoScrollEnabled(true);
      }

      // 메시지 상태 업데이트
      setMessages(prevMessages => [...prevMessages, data]);

      // 감정 색상 업데이트
      if (data.property?.emotion_hex_color) {
        setHeaderColor(data.property.emotion_hex_color);
      }
    });

    socket.on('disconnect', () => {
      console.log('웹소켓 연결 해제됨');
    });

    return () => {
      socket.disconnect();
    };
  }, [isAuthenticated, chatroomId]);

  // 스크롤 위치를 확인하는 함수
  const checkIfNearBottom = () => {
    const scrollContainer = scrollContainerRef.current;
    if (scrollContainer) {
      const { scrollTop, scrollHeight, clientHeight } = scrollContainer;
      const scrollPosition = scrollHeight - scrollTop - clientHeight;
      console.log('스크롤 위치:', scrollPosition);
      return scrollPosition < 200;
    }
    return true;
  };

  // 스크롤 이벤트 핸들러
  useEffect(() => {
    const scrollContainer = scrollContainerRef.current;
    
    const handleScroll = () => {
      if (scrollContainer) {
        const isBottom = checkIfNearBottom();
        
        // 사용자가 직접 스크롤해서 하단으로 갔다면 자동 스크롤 활성화
        if (isBottom) {
          setAutoScrollEnabled(true);
        }
      }
    };
    
    if (scrollContainer) {
      scrollContainer.addEventListener('scroll', handleScroll);
      return () => scrollContainer.removeEventListener('scroll', handleScroll);
    }
  }, []);

  // 메시지가 추가되면 스크롤 처리
  useEffect(() => {
    if (isInitialLoad) {
      scrollToBottomInstantly();
      setIsInitialLoad(false);
    } else {
      if (messages.length > 0) {
        if (autoScrollEnabled) {
          scrollToBottom();
        }
      }  
    }
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const scrollToBottomInstantly = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'auto' });
  };

  const closeToast = () => {
    console.log('토스트 닫기');
    setShowNewMessageToast(false);
  };

  const handleToastClick = () => {
    setAutoScrollEnabled(true);
    scrollToBottom();
    closeToast();
  };

  const initializeChatroom = async () => {
    try {
      setIsLoading(true);
      const chatrooms = await getChatrooms();
      
      if (chatrooms.length > 0) {
        const latestChatroom = chatrooms.reduce((latest, current) => {
          return new Date(current.created_at) > new Date(latest.created_at)
            ? current
            : latest;
        });
        
        setChatroomId(latestChatroom.id);
        if (latestChatroom.property?.latest_emotion_color) {
          setHeaderColor(latestChatroom.property.latest_emotion_color);
        }
        loadMessages(latestChatroom.id);
      }
    } catch (error) {
      setError('채팅방 초기화에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateChatroom = async () => {
    try {
      setIsLoading(true);
      const chatroom = await createChatroom();
      setChatroomId(chatroom.id);
      if (chatroom.property?.latest_emotion_color) {
        setHeaderColor(chatroom.property.latest_emotion_color);
      }
      loadMessages(chatroom.id);
    } catch (error) {
      setError('채팅방 생성에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const loadMessages = async (roomId: number) => {
    try {
      setIsInitialLoad(true);
      const chats = await getChats(roomId);
      setAutoScrollEnabled(false);
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
      setAutoScrollEnabled(true);
      setIsWaitingForBotMessage(true);
      const chat = await sendChat(chatroomId, newMessage);
      setMessages([...messages, chat]);
      setNewMessage('');
    } catch (error) {
      setError('메시지 전송에 실패했습니다.');
      setIsWaitingForBotMessage(false);
    }
  };

  const buildFormattedMessage = (message: Chat) => {
    if (!message.content) return '';
    return message.content.text.replace(/\\n/g, '\n');
  };

  if (isLoading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center">
        <div className="loading loading-spinner loading-lg"></div>
      </main>
    );
  }

  if (!chatroomId) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-24">
        <div className="card w-96 bg-base-100 shadow-xl">
          <div className="card-body items-center text-center">
            <h1 className="card-title text-2xl font-bold mb-4">새로운 대화 시작하기</h1>
            <p className="mb-6">새로운 대화방을 만들어보세요</p>
            <button 
              onClick={handleCreateChatroom} 
              className="btn btn-primary btn-lg"
              disabled={isLoading}
            >
              대화방 만들기
            </button>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="flex flex-col h-screen">
      {/* 상단 고정 영역 */}
      <header className="sticky top-0 z-10 border-b border-base-300 bg-base-100 shadow-sm flex flex-col">
        <div className="flex flex-row">
          <div className="flex-1"></div>
          <div className="flex items-center px-4">
            <button onClick={handleLogout} className="btn btn-ghost">
              로그아웃
            </button>
          </div>
        </div>

        {error && (
          <div className="alert alert-error mx-4 mb-2">
            <span>{error}</span>
          </div>
        )}
      </header>
      
      {/* 스크롤 가능한 메시지 영역 */}
      <div className="flex-1 overflow-y-auto px-4 relative" ref={scrollContainerRef}>
        <div className="max-w-4xl mx-auto w-full space-y-4 py-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender_type === 'user' ? 'justify-end' : 'justify-start'
              } flex-row gap-4`}
            >
              <div
                className={`max-w-[75%] p-4 rounded-lg whitespace-pre-wrap ${
                  message.sender_type === 'user'
                    ? 'bg-primary text-primary-content'
                    : 'bg-base-200'
                }`}
              >
                {buildFormattedMessage(message)}
              </div>
              
              {message.sender_type !== 'user' && message.property?.emoticon && (
                <div className="flex flex-col p-1">
                  <div className="flex-1"></div>
                  <div className="flex justify-end mt-2 text-sm font-[500] animate-spring-scale font-notoSansJP">
                    {message.property.emoticon}
                  </div>
                </div>
              )}

            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* 봇 응답 대기 메시지 */}
      {isWaitingForBotMessage && (
        <div className="px-4 py-2">
          <div className="max-w-4xl mx-auto">
            <div className="flex justify-start">
              <div className="bg-base-200 p-4 rounded-lg">
                <span className="rainbow-text">응답을 쓰는 중...</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 하단 고정 입력 영역 */}
      <footer className="sticky bottom-0 bg-base-100 border-t border-base-300 flex flex-col">
        <div className="h-2 transition-colors duration-1000" style={{ backgroundColor: headerColor }}></div>
        <div className="max-w-4xl mx-auto w-full p-4">
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
      </footer>

      {/* 토스트 메시지 (스크롤과 독립적으로 표시) */}
      {showNewMessageToast && latestMessage && (
        <div 
          className="fixed bottom-20 left-1/2 transform -translate-x-1/2 bg-base-100 text-base-content p-3 rounded-lg shadow-lg cursor-pointer z-50 max-w-xs w-full border border-primary"
          onClick={handleToastClick}
        >
          <div className="flex flex-col">
            <div className="flex justify-between items-center mb-1">
              <span className="font-bold text-sm text-primary">새 메시지</span>
              <button 
                onClick={(e) => {
                  e.stopPropagation();
                  closeToast();
                }}
                className="text-xs text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            <span className="text-sm line-clamp-2">{buildFormattedMessage(latestMessage)}</span>
          </div>
        </div>
      )}
    </main>
  );
}