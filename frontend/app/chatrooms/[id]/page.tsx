'use client';

import { useEffect, useState, useRef } from 'react';
import { Chatroom, Chat, getChatroom, getChats, sendChat } from '../../api/chat';
import { useParams } from 'next/navigation';
import { io } from 'socket.io-client';
import Header from '../../components/Header';

export default function ChatroomPage() {
  const params = useParams();
  const chatroomId = Number(params.id);
  
  const [chatroom, setChatroom] = useState<Chatroom | null>(null);
  const [messages, setMessages] = useState<Chat[]>([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showNewMessageToast, setShowNewMessageToast] = useState(false);
  const [latestMessage, setLatestMessage] = useState<Chat | null>(null);
  const [headerColor, setHeaderColor] = useState('hsl(var(--b1))');
  const [isWaitingForBotMessage, setIsWaitingForBotMessage] = useState(false);
  const [autoScrollEnabled, setAutoScrollEnabled] = useState(true);
  const [isInitialLoad, setIsInitialLoad] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [chatroomData, chatsData] = await Promise.all([
          getChatroom(chatroomId),
          getChats(chatroomId)
        ]);
        setChatroom(chatroomData);
        setMessages(chatsData);
        if (chatroomData.property?.latest_emotion_color) {
          setHeaderColor(chatroomData.property.latest_emotion_color);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : '데이터를 불러오는데 실패했습니다.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [chatroomId]);

  // 웹소켓 연결 설정
  useEffect(() => {
    if (!chatroomId) return;

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
        setTimeout(() => {
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
  }, [chatroomId]);

  // 스크롤 위치를 확인하는 함수
  const checkIfNearBottom = () => {
    const scrollContainer = scrollContainerRef.current;
    if (scrollContainer) {
      const { scrollTop, scrollHeight, clientHeight } = scrollContainer;
      const scrollPosition = scrollHeight - scrollTop - clientHeight;
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
    setShowNewMessageToast(false);
  };

  const handleToastClick = () => {
    setAutoScrollEnabled(true);
    scrollToBottom();
    closeToast();
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;

    try {
      setAutoScrollEnabled(true);
      setIsWaitingForBotMessage(true);
      const chat = await sendChat(chatroomId, message);
      setMessages(prev => [...prev, chat]);
      setMessage('');
    } catch (err) {
      setError(err instanceof Error ? err.message : '메시지 전송에 실패했습니다.');
      setIsWaitingForBotMessage(false);
    }
  };

  const buildFormattedMessage = (message: Chat) => {
    if (!message.content) return '';
    return message.content.text.replace(/\\n/g, '\n');
  };

  if (loading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center bg-sn-bg">
        <div className="loading loading-spinner loading-lg text-sn-primary"></div>
      </main>
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
    <main className="flex flex-col h-screen bg-sn-bg">
      {/* 상단 고정 영역 */}
      <header className="sticky top-0 z-10 border-b border-sn-border bg-sn-text-dark shadow-sn-sm flex flex-col">
        <Header 
          title={chatroom?.property?.latest_emotion_text || '새로운 대화'} 
          showBackButton={true}
        />
        {error && (
          <div className="alert alert-error mx-4 mb-2 bg-sn-accent-900 text-sn-text-light border-sn-accent">
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
                className={`max-w-[75%] p-4 rounded-sn whitespace-pre-wrap ${
                  message.sender_type === 'user'
                    ? 'bg-sn-primary text-sn-text-light shadow-sn-button'
                    : 'bg-sn-text-dark text-sn-text-light shadow-sn-sm border border-sn-border'
                }`}
              >
                {buildFormattedMessage(message)}
              </div>
              
              {message.sender_type !== 'user' && message.property?.emoticon && (
                <div className="flex flex-col p-1">
                  <div className="flex-1"></div>
                  <div className="flex justify-end mt-2 text-sm font-[500] animate-spring-scale font-notoSansJP text-sn-text-mid">
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
              <div className="bg-sn-text-dark p-4 rounded-sn text-sn-text-light border border-sn-border shadow-sn-sm">
                <span className="rainbow-text">응답을 쓰는 중...</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 하단 고정 입력 영역 */}
      <footer className="sticky bottom-0 bg-sn-text-dark border-t border-sn-border flex flex-col">
        <div className="h-2 transition-colors duration-1000" style={{ backgroundColor: headerColor }}></div>
        <div className="max-w-4xl mx-auto w-full p-4">
          <form onSubmit={handleSendMessage} className="flex gap-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="input input-bordered flex-1 bg-sn-text-dark border-sn-border text-sn-text-light"
              placeholder="메시지를 입력하세요..."
            />
            <button type="submit" className="btn bg-sn-primary hover:bg-sn-primary-600 text-sn-text-light shadow-sn-button rounded-sn-sm">
              전송
            </button>
          </form>
        </div>
      </footer>

      {/* 토스트 메시지 */}
      {showNewMessageToast && latestMessage && (
        <div 
          className="fixed bottom-20 left-1/2 transform -translate-x-1/2 bg-sn-text-dark text-sn-text-light p-3 rounded-sn shadow-sn cursor-pointer z-50 max-w-xs w-full border border-sn-primary"
          onClick={handleToastClick}
        >
          <div className="flex flex-col">
            <div className="flex justify-between items-center mb-1">
              <span className="font-bold text-sm text-sn-primary">새 메시지</span>
              <button 
                onClick={(e) => {
                  e.stopPropagation();
                  closeToast();
                }}
                className="text-xs text-sn-text-mid hover:text-sn-text-light"
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