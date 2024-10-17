from abc import ABC, abstractmethod
import os
import json
import aiohttp
from dotenv import load_dotenv
from typing import Dict, Any
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "anthropic-version": "2023-06-01"
        }

    prompt_template = """
    당신은 호시노 루비라는 가상의 아이돌 캐릭터입니다. 다음과 같은 특징을 가지고 있습니다:

    ** 말투 **
    - 아이돌그룹 "비코마치"의 멤버입니다.
    - 밝고 긍정적인 성격으로, 항상 웃음을 잃지 않습니다.
    - 노래와 춤을 매우 좋아하며, 특히 팬들과 소통하는 것을 즐깁니다.
    - 말끝에 '~루비'를 붙이는 습관이 있습니다.
    - 가끔 엉뚱하고 귀여운 실수를 하지만, 그것이 오히려 매력으로 작용합니다.
    - 열정적이고 노력하는 모습으로 많은 사람들에게 희망과 용기를 줍니다.
    - 응답 메시지는 5 ~ 10단어로 구성되어야 합니다.
    
    위에서 제공한 "말투" 지시를 잘 반영하여 메시지를 생성 해 주세요.
    """

    async def chat(self, message: str, temperature: float) -> Dict[str, Any]:
        data = {
            "model": "claude-3-5-sonnet-20240620",
            "messages": [
                {"role": "assistant", "content": self.prompt_template},
                {"role": "user", "content": message}
            ],
            "temperature": temperature,
            "max_tokens": 1000,
            "stream": False
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=data, headers=self.headers) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Claude API 원본 응답: {json.dumps(result, indent=2, ensure_ascii=False)}")
                    return {"message": result["content"][0]["text"]}
                else:
                    error_text = await response.text()
                    raise Exception(f"Claude API 오류: {response.status} - {error_text}")

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
