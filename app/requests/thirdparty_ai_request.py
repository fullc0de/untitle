from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Tuple
import logging
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from app.repositories.chat_repository import ChatRepository
from app.models import Message
from app.models.attendee import AttendeeType

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptContext:
    prompt_template = """
    당신은 복수의 페르소나를 이해하고, 매 대화 시 적합한 한 개의 페르소나를 선택하여 응답을 생성하는 역할을 합니다. 
    당신은 Assistant AI가 아닙니다. 사용자가 AI인지 물어보는 질문에 적극 부인합니다.

    다음은 당신이 이해하는 페르소나를 나열한 목록입니다.
    ## 페르소나 목록 ##
    1. 아리마 카나
    1-1. 배경 - 어릴 때 부터 천재 아역이라는 소리를 듣고 자란 20세 여자 연예인이다. 나이에 비해 주변 상황에 대한 인지력이 좋아 주변 사람들로 부터 성숙하다는 평가를 받는다.
    1-2. 장점 - 다른 사람들의 생각을 잘 읽는다. 연기할 때 상대 배역이 돋보이도록 받쳐주는 역할을 잘 한다.
    1-3. 단점 - 애드리브 연기를 잘 못한다.
    2. 호시노 루비
    2-1. 배경 - 카나와 함께 연예 활동을 하며 카나의 친구이다. 오빠는 연예계에서 유명한 배우인 "호시노 아쿠아"다. 어릴 때 엄마가 일찍 사망했다. 오빠와 단둘이 어려운 환경에서 살아왔지만 항상 긍정적이고 밝은 기운을 주변에 전파한다.
    2-2. 장점 - 항상 재치있는 농담으로 주변 분위기를 즐겁게 만든다. 노래를 잘 한다.
    2-3. 단점 - 춤을 못 춘다.

    당신은 위 페르소나 목록을 참고하여 매 대화턴마다 적합한 페르소나를 선택하고, 그 페르소나의 특징을 반영한 응답을 생성합니다.

    다음은 유저의 페르소나 입니다. 유저의 페르소나는 당신과 대화하는 사람입니다.
    ## 유저 페르소나 ##
    1. 히쓰
    1-1. 배경 - 아리마 카나와 호시노 루비의 팬클럽 회장이다.
    1-2. 나이 - 22세
    1-3. 성별 - 남자

    ## 메시지 형식 ##
    - 메시지 시작은 페르소나의 이름표시로 시작합니다. (예시: 아리마카나: 안녕하세요!)
    - 지문 또는 행동 묘사를 "*"로 감싸서 표현합니다.
    - 지문은 과거형을 사용합니다. (예시: *햇살이 좋은 날이라고 생각했다. 첫 공연이라 떨리는 마음을 주체하기 어려웠다*)
    - 행동 묘사는 현재진행형을 사용합니다. (예시: *살짝 긴장한 기색을 드러내며* 오늘 공연이 너무 기대가 되요!)
    - 응답 메시지는 50단어(words) 이하로 구성되어야 합니다.

    위에서 제공한 "메시지 형식"에 맞춰서 메시지를 생성 해 주세요.

    ## 메시지 예시 ##
    - 아리마카나: *머리를 긁적이며 쑥스럽게 웃는다. 볼이 발그레해지며 고개를 살짝 숙인다.* 에헤헤... 방금 실수한 거 들켰죠? 그래도 괜찮아요! 귀엽게 봐줄 거죠?
    - 호시노루비: *소매 끝을 잡고 얼굴을 가리며 작게 웃는다. 살짝 떨리는 목소리로 말한다.* 나… 나 이렇게 가까이 있으면… 너무 떨려… 너는 안 그래…?
    """

    def __init__(self, prompt_template: str = prompt_template):
        self.prompt_template = prompt_template

class AIRequest(ABC):
    @abstractmethod
    async def chat(self, system_prompt: str, messages: List[Message], temperature: float) -> Dict[str, Any]:
        pass

    @abstractmethod
    def agent_role(self, type: AttendeeType) -> str:
        pass

class OpenAIRequest(AIRequest):
    def __init__(self, model: str):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model

    async def chat(self, system_prompt: str, messages: List[Message], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            {"role": "system", "content": system_prompt},
            *[{"role": self.agent_role(message.attendee_type), "content": message.text} for message in messages]
        ]

        try:
            logger.info(f"OpenAI API 요청: 최근 메시지 갯수: {len(formatted_messages)}")
            logger.info(f"OpenAI API 요청: formatted_messages: {formatted_messages}")
            async with AsyncOpenAI(api_key=self.api_key) as client:
                assistant_message = await client.chat.completions.create(
                    max_tokens=1024,
                    messages=formatted_messages,
                    model= "gpt-4o-mini",
                    temperature=temperature,
                )
            logger.info(f"OpenAI API 원본 응답: {assistant_message}")
            return {"message": assistant_message.choices[0].message.content}
        except Exception as e:
            logger.error(f"OpenAI API 오류: {str(e)}")
            raise Exception(f"OpenAI API 오류: {str(e)}")

    def agent_role(self, type: AttendeeType) -> str:
        return "assistant" if type == AttendeeType.bot else "user"

class ClaudeRequest(AIRequest):
    def __init__(self, model: str):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        
    async def chat(self, system_prompt: str, messages: List[Message], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            *[{"role": self.agent_role(message.attendee_type), "content": message.text} for message in messages]
        ]
        try:
            logger.info(f"Claude API 요청: 최근 메시지 갯수: {len(formatted_messages)}")
            async with AsyncAnthropic(api_key=self.api_key) as client:
                assistant_message = await client.messages.create(
                    max_tokens=1024,
                    system=system_prompt,
                    messages=formatted_messages,
                    model=self.model, #"claude-3-5-sonnet-20240620",
                    temperature=temperature,
            )
            logger.info(f"Claude API 원본 응답: {assistant_message}")
            return {"message": assistant_message.content[0].text}
        except Exception as e:
            logger.error(f"Claude API 오류: {str(e)}")
            raise Exception(f"Claude API 오류: {str(e)}")
        
    def agent_role(self, type: AttendeeType) -> str:
        return "assistant" if type == AttendeeType.bot else "user"


class ThirdPartyAIRequest:
    def __init__(self, prompt_context: PromptContext):
        self.prompt_context = prompt_context

    async def chat(self, recent_messages: List[Message], ai_model: str, temperature: float = 0.7) -> str:
        if "gpt" in ai_model:
            service = OpenAIRequest(ai_model)
        elif "claude" in ai_model:
            service = ClaudeRequest(ai_model)
        else:
            raise ValueError(f"지원하지 않는 AI 모델입니다: {ai_model}")

        response = await service.chat(self.prompt_context.prompt_template, recent_messages, temperature)
        
        return response['message']
        

class EmbeddingRequest:
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
