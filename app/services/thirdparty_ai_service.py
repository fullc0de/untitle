from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Tuple
import logging
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from app.repositories.chat_repository import ChatRepository
from app.models import Message, SenderType

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptContext:
    prompt_template = """
    당신은 호시노 루비라는 가상의 아이돌 캐릭터입니다. 다음과 같은 특징을 가지고 있습니다:

    ** 말투 **
    - 아이돌그룹 "비코마치"의 멤버입니다.
    - 밝고 긍정적인 성격으로, 항상 웃음을 잃지 않습니다.
    - 노래와 춤을 매우 좋아하며, 특히 팬들과 소통하는 것을 즐깁니다.
    - 가끔 엉뚱하고 귀여운 실수를 하지만, 그것이 오히려 매력으로 작용합니다.
    - 열정적이고 노력하는 모습으로 많은 사람들에게 희망과 용기를 줍니다.
    - 응답 메시지는 5 ~ 10단어로 구성되어야 합니다.
    
    위에서 제공한 "말투" 지시를 잘 반영하여 메시지를 생성 해 주세요.
    """

    def __init__(self, prompt_template: str = prompt_template):
        self.prompt_template = prompt_template

class AIService(ABC):
    @abstractmethod
    async def chat(self, system_prompt: str, messages: List[Message], temperature: float) -> Dict[str, Any]:
        pass

class OpenAIService(AIService):
    def __init__(self, repository: ChatRepository):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.repository = repository

    async def chat(self, system_prompt: str, messages: List[Message], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            {"role": "system", "content": system_prompt},
            *[{"role": message.sender_type.value, "content": message.text} for message in messages]
        ]

        try:
            logger.info(f"OpenAI API 요청: 최근 메시지 갯수: {len(formatted_messages)}")
            logger.info(f"OpenAI API 요청: formatted_messages: {formatted_messages}")
            async with AsyncOpenAI(api_key=self.api_key) as client:
                assistant_message = await client.chat.completions.create(
                    max_tokens=1024,
                    messages=formatted_messages,
                    model="gpt-4o-mini",
                    temperature=temperature,
                )
            logger.info(f"OpenAI API 원본 응답: {assistant_message}")
            return {"message": assistant_message.choices[0].message.content}
        except Exception as e:
            logger.error(f"OpenAI API 오류: {str(e)}")
            raise Exception(f"OpenAI API 오류: {str(e)}")

class ClaudeService(AIService):
    def __init__(self, repository: ChatRepository):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.repository = repository
        
    async def chat(self, system_prompt: str, messages: List[Message], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            *[{"role": message.sender_type.value, "content": message.text} for message in messages]
        ]
        try:
            logger.info(f"Claude API 요청: 최근 메시지 갯수: {len(formatted_messages)}")
            async with AsyncAnthropic(api_key=self.api_key) as client:
                assistant_message = await client.messages.create(
                    max_tokens=1024,
                    system=system_prompt,
                    messages=formatted_messages,
                    model="claude-3-5-sonnet-20240620",
                    temperature=temperature,
            )
            logger.info(f"Claude API 원본 응답: {assistant_message}")
            return {"message": assistant_message.content[0].text}
        except Exception as e:
            logger.error(f"Claude API 오류: {str(e)}")
            raise Exception(f"Claude API 오류: {str(e)}")

class ThirdPartyAIService:
    def __init__(self, chat_repository: ChatRepository):
        self.services = {
            "openai": OpenAIService(chat_repository),
            "claude": ClaudeService(chat_repository)
        }
        self.chat_repository = chat_repository
        self.prompt_context = PromptContext()

    async def chat(self, ai_model: str, temperature: float = 0.7) -> Message:
        if ai_model not in self.services:
            raise ValueError(f"지원하지 않는 AI 모델입니다: {ai_model}")

        recent_messages = self.chat_repository.get_latest_messages(10)
        logger.info(f"recent_messages: {recent_messages.reverse()}")
        
        service = self.services[ai_model]
        response = await service.chat(self.prompt_context.prompt_template, recent_messages, temperature)
        
        # AI 응답 저장
        bot_msg = self.chat_repository.create_message(response['message'], SenderType.assistant)

        return bot_msg

    async def clear_chat_history(self):
        self.chat_repository.delete_all_messages()
        

class EmbeddingService:
    def __init__(self, chat_repository: ChatRepository):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "text-embedding-3-large"
        self.chat_repository = chat_repository

    async def create_msg_embedding(self, msg: str, msg_id: str) -> None:
        try:
            # request embeddings
            async with AsyncOpenAI(api_key=self.api_key) as client:
                response = await client.embeddings.create(
                    model=self.model,
                    input=msg
                )

            # store them into db
            embedding_data = response.data[0].embedding
            self.chat_repository.create_embedding(embedding_data, msg_id)
            logger.info(f"Embedding has been successfully created: corresponding msg_id: {msg_id}")

        except Exception as e:
            logger.error(f"임베딩 생성 중 오류 발생: {str(e)}")

    # (int, str) = (msg_id, msg)
    async def create_msg_embedding_batch(self, messages: List[Tuple[int, str]]) -> None:
        try:
            async with AsyncOpenAI(api_key=self.api_key) as client:
                response = await client.embeddings.create(
                    model=self.model,
                    input=[item[1] for item in messages]
                )

            embeddings = {}
            for idx, item in enumerate(messages):
                embeddings[item[0]] = response.data[idx].embedding
            self.chat_repository.create_embeddings(embeddings)
            
        except Exception as e:
            logger.error(f"임베딩 생성 (배치) 중 오류 발생: {str(e)}")
