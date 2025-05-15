from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class CharacterFacts(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    current_emotion: str
    relationship: Optional[str] = None
    interests: Optional[str] = None
    expertise: Optional[str] = None
    newly_established_fact_on_both_user_and_character: Optional[str] = None

    @classmethod
    def json_schema(cls) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "당신의 이름"
                },
                "gender": {
                    "type": "string",
                    "description": "당신의 성별"
                },
                "relationship": {
                    "type": "string",
                    "description": "유저와 당신의 현재 관계"
                },
                "interests": {
                    "type": "string",
                    "description": "당신의 관심사 (취미, 기호)"
                },
                "expertise": {
                    "type": "string",
                    "description": "당신의 전문 분야 (직업, 특기, 지식)"
                },
                "current_emotion": {
                    "type": "string",
                    "description": "현재 당신이 느끼는 감정"
                },
                "newly_established_fact_on_both_user_and_character": {
                    "type": "string",
                    "description": "당신과 유저 모두에 관련되어 새롭게 [합의, 정의, 부여, 발견]된 사실이나 정보"
                }
            },
            "required": ["current_emotion"]
        }
    

class CharacterJsonResponse(BaseModel):
    message: str
    character_facts: CharacterFacts

    @classmethod
    def json_schema(cls) -> Dict[str, Any]:
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "character_json_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "캐릭터가 생성한 응답 메시지"
                        },
                        "character_facts": CharacterFacts.json_schema()
                    },
                    "required": ["message", "character_facts"]
                }
            }
        }


class CharacterResponse(BaseModel):
    name: str
    #attendee_id: Optional[int] = None
    is_main_character: bool
    is_storyteller: bool
    message: str

class ChatbotInfo(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    relationship: Optional[str] = None
    interest_keywords: Optional[List[str]] = None
    expertise_keywords: Optional[List[str]] = None

    @classmethod
    def json_schema(cls) -> Dict[str, Any]:
        return {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "챗봇 이름"},
                    "gender": {"type": "string", "description": "챗봇 성별"},
                    "relationship": {"type": "string", "description": "챗봇과 유저의 관계"},
                    "interest_keywords": {"type": "array", "items": {"type": "string"}, "description": "챗봇의 관심 분야 (키워드)"},
                    "expertise_keywords": {"type": "array", "items": {"type": "string"}, "description": "챗봇의 전문 분야 (키워드)"}
                },
                "required": ["name", "gender", "relationship", "interest_keywords", "expertise_keywords"]
            }
        }
                
class SummaryResponse(BaseModel):
    facts_summary: str
    chatbot_info: ChatbotInfo

    @classmethod
    def json_schema(cls) -> Dict[str, Any]:
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "summary_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "facts_summary": {"type": "string"},
                        "chatbot_info": ChatbotInfo.json_schema()
                    },
                    "required": ["facts_summary", "chatbot_info"]
                }
            }
        }
    
class AIResponse(BaseModel):
    messages: List[CharacterResponse]
    summary: str

    @classmethod
    def json_schema(cls) -> Dict[str, Any]:
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "ai_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "messages": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "캐릭터의 이름"
                                    },
                                    "is_main_character": {
                                        "type": "boolean",
                                        "description": "주인공 여부"
                                    },
                                    "is_storyteller": {
                                        "type": "boolean",
                                        "description": "내레이터 여부"
                                    },
                                    "message": {
                                        "type": "string",
                                        "description": "캐릭터의 메시지"
                                    }
                                },
                                "required": ["name", "is_main_character", "is_storyteller", "message"]
                            }
                        },
                        "summary": {
                            "type": "string",
                            "description": "대화 요약"
                        }
                    },
                    "required": ["messages", "summary"]
                }
            }
        }