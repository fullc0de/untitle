import { apiConfig } from '../config/api';

interface BotResp {
  id: number;
  name: string | null;
  // 필요한 다른 bot 관련 필드들 추가
}

export interface Chatroom {
  id: number;
  title: string | null;
  property: Record<string, any> | null;
  owner_id: number;
  created_at: string;
  updated_at: string;
  bot: BotResp | null;
}

export interface Chat {
  id: number;
  content: Record<string, any> | null;
  property: Record<string, any> | null;
  chatroom_id: number;
  sender_id: number;
  sender_type: 'user' | 'bot';
  created_at: string;
  updated_at: string;
}

export const createChatroom = async (): Promise<Chatroom> => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('인증되지 않은 사용자입니다.');
  }

  const response = await fetch(`${apiConfig.baseURL}/api/chatrooms`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('채팅방 생성에 실패했습니다.');
  }

  return response.json();
};

export const getChatrooms = async (): Promise<Chatroom[]> => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('인증되지 않은 사용자입니다.');
  }

  const response = await fetch(`${apiConfig.baseURL}/api/chatrooms`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('채팅방 목록을 가져오는데 실패했습니다.');
  }

  return response.json();
};

export const getChatroom = async (chatroomId: number): Promise<Chatroom> => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('인증되지 않은 사용자입니다.');
  }

  const response = await fetch(`${apiConfig.baseURL}/api/chatrooms/${chatroomId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('채팅방 정보를 가져오는데 실패했습니다.');
  }

  return response.json();
};

export const getChats = async (chatroomId: number): Promise<Chat[]> => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('인증되지 않은 사용자입니다.');
  }

  const response = await fetch(`${apiConfig.baseURL}/api/chats?chatroom_id=${chatroomId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('채팅 메시지를 가져오는데 실패했습니다.');
  }

  return response.json();
};

export const sendChat = async (
  chatroomId: number,
  text: string
): Promise<Chat> => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('인증되지 않은 사용자입니다.');
  }

  const response = await fetch(`${apiConfig.baseURL}/api/chats`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      chatroom_id: chatroomId,
      text,
    }),
  });

  if (!response.ok) {
    throw new Error('메시지 전송에 실패했습니다.');
  }

  return response.json();
}; 