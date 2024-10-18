from abc import ABC, abstractmethod
import os
import json
import aiohttp
from dotenv import load_dotenv
from typing import Dict, List, Any
import logging
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 테스트 목적
class ChatHistory:
    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages.clear()


class AIService(ABC):
    @abstractmethod
    async def chat(self, message: str, temperature: float) -> Dict[str, Any]:
        pass
    @abstractmethod
    async def clear_chat_history(self, ai_model: str):
        pass

class OpenAIService(AIService):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.chat_history = ChatHistory()

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
        # OpenAI API 호출 로직 구현
        self.chat_history.add_message("user", message)
        
        messages = [
            {"role": "system", "content": self.prompt_template},
            *self.chat_history.get_messages()
        ]

        try:
            logger.info(f"OpenAI API 요청: {messages}")
            async with AsyncOpenAI(api_key=self.api_key) as client:
                assistant_message = await client.chat.completions.create(
                    max_tokens=1024,
                    messages=messages,
                    model="gpt-4o-mini",
                    temperature=temperature,
                )
            logger.info(f"Claude API 원본 응답: {assistant_message}")
            self.chat_history.add_message("assistant", assistant_message.choices[0].message.content)
            return {"message": assistant_message.choices[0].message.content}
        except Exception as e:
            logger.error(f"OpenAI API 오류: {str(e)}")
            raise Exception(f"OpenAI API 오류: {str(e)}")

    async def clear_chat_history(self, ai_model: str):
        self.chat_history.clear()

class ClaudeService(AIService):
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.chat_history = ChatHistory()

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
        self.chat_history.add_message("user", message)
        
        messages = [
            *self.chat_history.get_messages()
        ]

        try:
            logger.info(f"Claude API 요청: {messages}")
            async with AsyncAnthropic(api_key=self.api_key) as client:
                assistant_message = await client.messages.create(
                    max_tokens=1024,
                system=self.prompt_template,
                messages=messages,
                model="claude-3-5-sonnet-20240620",
                temperature=temperature,
            )
            logger.info(f"Claude API 원본 응답: {assistant_message}")
            self.chat_history.add_message("assistant", assistant_message.content[0].text)
            return {"message": assistant_message.content[0].text}
        except Exception as e:
            logger.error(f"Claude API 오류: {str(e)}")
            raise Exception(f"Claude API 오류: {str(e)}")

    async def clear_chat_history(self, ai_model: str):
        self.chat_history.clear()

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

    async def clear_chat_history(self, ai_model: str):
        if ai_model not in self.services:
            raise ValueError(f"지원하지 않는 AI 모델입니다: {ai_model}")

        service = self.services[ai_model]
        await service.clear_chat_history(ai_model)
