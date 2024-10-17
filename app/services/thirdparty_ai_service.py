from abc import ABC, abstractmethod
import json
from typing import Dict, Any

class AIService(ABC):
    @abstractmethod
    async def chat(self, message: str, temperature: float) -> Dict[str, Any]:
        pass

class OpenAIService(AIService):
    async def chat(self, message: str, temperature: float) -> Dict[str, Any]:
        # OpenAI API 호출 로직 구현
        # 실제 구현 시 aiohttp 등을 사용하여 비동기 요청 수행
        return {"message": "Hello, World!"}

class ClaudeService(AIService):
    async def chat(self, message: str, temperature: float) -> Dict[str, Any]:
        # Claude API 호출 로직 구현
        # 실제 구현 시 aiohttp 등을 사용하여 비동기 요청 수행
        return {"message": "Hello, World!"}

class ThirdPartyAIService:
    def __init__(self):
        self.services = {
            "openai": OpenAIService(),
            "claude": ClaudeService()
        }

    async def chat(self, ai_model: str, message: str, temperature: float = 0.7) -> Dict[str, Any]:
        if ai_model not in self.services:
            raise ValueError(f"지원하지 않는 AI 모델입니다: {ai_model}")

        service = self.services[ai_model]
        response = await service.chat(message, temperature)
        
        return json.dumps(response)
