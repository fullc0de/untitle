from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class CharacterFacts(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    current_emotion: str
    relationship: Optional[str] = None
    interests: Optional[str] = None
    expertise: Optional[str] = None
    newly_defined_fact: Optional[str] = None

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
                        "character_facts": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "캐릭터 이름"
                                },
                                "gender": {
                                    "type": "string",
                                    "description": "캐릭터의 성별"
                                },
                                "relationship": {
                                    "type": "string",
                                    "description": "유저에 대한 캐릭터의 현재 관계"
                                },
                                "interests": {
                                    "type": "string",
                                    "description": "캐릭터의 관심사"
                                },
                                "expertise": {
                                    "type": "string",
                                    "description": "캐릭터의 전문 분야"
                                },
                                "current_emotion": {
                                    "type": "string",
                                    "description": "현재 캐릭터가 느끼는 감정"
                                },
                                "newly_defined_fact": {
                                    "type": "string",
                                    "description": "최근 대화를 통해 유저가 캐릭터에게 부여한 정의"
                                }
                            },
                            "required": ["current_emotion"]
                        }
                    },
                    "required": ["message", "facts"]
                }
            }
        }


class CharacterResponse(BaseModel):
    name: str
    #attendee_id: Optional[int] = None
    is_main_character: bool
    is_storyteller: bool
    message: str

class CharacterInfo(BaseModel):
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
                    "name": {"type": "string", "description": "캐릭터 이름"},
                    "gender": {"type": "string", "description": "캐릭터 성별"},
                    "relationship": {"type": "string", "description": "캐릭터와 유저의 관계"},
                    "interest_keywords": {"type": "array", "items": {"type": "string"}, "description": "캐릭터의 관심 분야 (키워드)"},
                    "expertise_keywords": {"type": "array", "items": {"type": "string"}, "description": "캐릭터의 전문 분야 (키워드)"}
                },
                "required": ["name", "gender", "relationship", "interest_keywords", "expertise_keywords"]
            }
        }
                
class SummaryResponse(BaseModel):
    summary: str
    character_info: CharacterInfo

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
                        "summary": {"type": "string"},
                        "character_info": CharacterInfo.json_schema()
                    },
                    "required": ["summary", "character_info"]
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