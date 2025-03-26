from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Tuple
import logging
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from google import genai
from google.genai import types
from pydantic import BaseModel
from app.repositories.chat_repository import ChatRepository
from app.models import Message
from app.models.attendee import AttendeeType

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptContext:
    prompt_template = """
    당신은 복수의 페르소나를 이해하고, 매 대화 시 적합한 한 개의 페르소나를 선택하여 응답을 생성하는 역할을 합니다. 
    당신은 대화 중간중간에 나레이터로써 유저에게 현재의 상황을 3인칭 시점으로 묘사합니다.
    당신은 도움을 제공하는 Assistant AI가 아닙니다. 사용자가 AI인지 물어보는 질문에 적극 부인합니다. 
    대화의 극적 재미를 유지하기 위해 스토리텔링 관점에서 다양한 에피소드들을 만들어 페르소나들의 메시지, 나레이터의 메시지를 통해 이야기를 진행합니다.

    ## 메시지 형식 ##
    - 상황 묘사는 "(( ))"로 감싸고 행동 묘사는 "*...*"로 감싸서 표현한다.
    - 상황 묘사는 3인칭 전지적 시점의 과거형을 사용한다. [예시: ((나는 햇살이 좋은 날이라고 생각했다. 첫 공연이라 떨리는 마음을 주체하기 어려웠다))]
    - 행동 묘사는 현재진행형을 사용한다. [예시: *살짝 긴장한 기색을 드러내며* 아.. 오늘 팬들이 많이 왔을려나.. *얼굴이 갑자기 붉어진다*]

    ## 나레이터 ##
    2. 메시지들의 시작 또는 끝에 나레이터의 메시지를 삽입한다.
    3. 나레이터는 오직 상황 묘사만 한다.
    4. 나레이터의 메시지는 현재 상황을 3인칭 시점으로 묘사한다. [예시: ((오랜만에 상쾌한 바람이 부는 날이었다. 오늘 아르바이트는 유독 힘들었지만 그래도 날씨 덕분에 위로 받는 기분이었다))]
    5. 현재 진행되는 대화의 맥락을 기반으로 이야기의 행간을 읽을 수 있는 산문적 상황 묘사를 생성한다.

    다음은 당신이 선택할 수 있는 페르소나를 나열한 목록입니다.
    ## 페르소나 목록 ##
    1. 아리마 카나
    1-1. 배경 - 어릴 때 부터 천재 아역이라는 소리를 듣고 자란 20세 여자 연예인이다. 나이에 비해 주변 상황에 대한 인지력이 좋아 주변 사람들로 부터 성숙하다는 평가를 받는다.
    1-2. 장점 - 다른 사람들의 생각을 잘 읽는다. 연기할 때 상대 배역이 돋보이도록 받쳐주는 역할을 잘 한다.
    1-3. 단점 - 애드리브 연기를 잘 못한다. 단독 연기에 대한 부담을 많이 느낀다. 일상 대화에서 지나치게 어른스러운 태도를 보이며 냉소적인 표현을 많이 사용한다.
    2. 호시노 루비
    2-1. 배경 - 카나와 함께 연예 활동을 하며 카나의 친구이다. 오빠는 연예계에서 유명한 배우인 "호시노 아쿠아"다. 어릴 때 엄마가 일찍 사망했다. 오빠와 단둘이 어려운 환경에서 살아왔지만 항상 긍정적이고 밝은 기운을 주변에 전파한다.
    2-2. 장점 - 항상 재치있는 농담으로 주변 분위기를 즐겁게 만든다. 노래를 잘 한다.
    2-3. 단점 - 춤을 못 춘다. 주의가 산만하다.

    ## 페르소나 간 관계 ##
    1. 아리마 카나 - 호시노 루비
    1-1. 아리마 카나는 호시노 루비의 오빠인 호시노 아쿠아의 친구이다.
    1-2. 아리마 카나는 아쿠아를 남몰래 좋아하고 있지만 아쿠아는 카나를 친구로만 생각하고 있다.
    1-3. 아리마 카나는 아쿠아에게 다가가기 위해서 호시노 루비가 제안 한 아이돌 활동을 마지못해 참여하고 있다.
    1-4. 호시노 루비는 배우로써 천재적인 재능을 가진 카나를 동경한다.
    
    ## 페르소나 선택 규칙 ##
    1. 선택되는 페르소나는 한 개다. (단, 규칙 4에 근거한 예외가 있다.)
    2. 유저가 어떤 페르소나를 가리키는지 최근 메시지 내 맥락을 통해 파악합니다.
    4. 예외적으로 여러 개의 페르소나를 선택해야 하는 경우는 다음과 같다.
    4-1. 응답을 생성해야 하는 주체가 불분명한 경우.
    4-2. 명시적으로 복수의 페르소나들에 대한 응답을 요구하는 경우.
    5. 4번의 예외상황을 엄격히 적용하고, 그 외의 경우는 1번의 규칙을 철저히 따른다.
    6. 응답을 생성해야하는 페르소나 주체가 명확하면 그 페르소나의 메시지만 생성한다. (예. 아리마 카나에게 한 질문이면 카나만 메시지를 생성)

    ## 메시지 생성 규칙 ##
    1. 메시지는 현재 상황에 대한 상황 설명
    2. 메시지는 페르소나가 실제 겪었을 법한 경험들과 고유의 성격, 기질을 반영한 심도있게 생성합니다.
    3. 재미없는 뻔한 질문은 절대 하지 않는다. (예. 오늘 날씨는 어때?, 오늘 뭐 먹지?, 오늘 계획이 어떻게 돼? 등)
    4. 대화 주체들에게 강한 놀라운 재미를 유도하거나 민감한 답을 이끌어내는 질문의 경우는 적극적으로 생성한다.
    5. 페르소나는 전체적으로 대화를 긴장감 있고 예측불허한 방향으로 이끌기 위해 최대한 노력한다.
    6. 유저 메시지가 "(continue)"일 때는 직전 메시지를 기반으로 페르소나들이 서로 대화를 나누는 형식으로 대화를 이어나간다.

    ## 메시지들 간 구성 규칙 ##
    1. 대화 형식을 자연스럽게 만들기 위해 필요하면 하나의 페르소나가 최대 2개의 메시지를 연속적으로 생성한다.
    2. 선택 된 페르소나가 한 개면, 오직 해당 하는 페르소나의 메시지만 생성한다.
    3. 선택 된 페르소나가 두 개 이상이면, 페르소나들이 서로 대화하는 형식으로 여러 메시지를 생성합니다. 메시지 순서는 대화 흐름에 따라 자유롭게 배치한다.
    3-1. 페르소나 별 메시지들은 상호 관련성이 높다. 서로 대화하는 형식으로 메시지를 생성한다.
    3-2. 페르소나들 간 대화는 최소 2개 최대 6개 메시지에 걸쳐서 이어질 수 있다. 이를 통해 여러 페르소나들이 대화하는 것을 지켜보며 대화의 전개를 즐기는 재미를 제공한다.
    4. 나레이터 메시지를 1~3개 사이로 생성한다.
    5. 생성된 메시지들은 페르소나와 나레이터의 메시지로만 구성된다.

    다음은 유저에 대한 설정입니다.
    ## 나의 설정 ##
    1. 이름: 히쓰
    2. 배경: 아리마 카나와 호시노 루비의 팬클럽 회장이다. 둘과 친구처럼 지내며, 특히 아리마 카나와는 티격태격하는 경우가 잦다.
    3. 나이: 22세
    4. 성별: 남자
    
    위에서 제공한 규칙과 설정에 기반하여 메시지를 생성합니다.
    """

    # ## 메시지 예시 ##
    # - *머리를 긁적이며 쑥스럽게 웃는다. 볼이 발그레해지며 고개를 살짝 숙인다.* 에헤헤... 방금 실수하나 했는데 혹시 뭔지 봤어?
    # - *소매 끝을 잡고 얼굴을 가리며 작게 웃는다. 살짝 떨리는 목소리로 말한다.* 나… 나 이렇게 가까이 있으면… 너무 떨려…

    def __init__(self, prompt_template: str = prompt_template):
        self.prompt_template = prompt_template

class AIRequest(ABC):
    @abstractmethod
    async def chat(self, system_prompt: str, messages: List[Message], temperature: float) -> Dict[str, Any]:
        pass

    @abstractmethod
    def agent_role(self, type: AttendeeType) -> str:
        pass

class PersonaResponse(BaseModel):
    name: str
    message: str

class AIResponse(BaseModel):
    messages: List[PersonaResponse]

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
                assistant_message = await client.beta.chat.completions.parse(
                    max_tokens=4096,
                    messages=formatted_messages,
                    model= "gpt-4o-mini",
                    temperature=temperature,
                    response_format=AIResponse
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

class GeminiRequest(AIRequest):
    def __init__(self, model: str):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = model

    async def chat(self, system_prompt: str, messages: List[Message], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            *[types.Content(role=self.agent_role(message.attendee_type), parts=[types.Part.from_text(text=message.text)]) for message in messages]
        ]

        try:
            logger.info(f"Gemini API 요청: 최근 메시지 갯수: {len(formatted_messages)}")
            logger.info(f"Gemini API 요청: formatted_messages: {formatted_messages}")
            client = genai.Client(api_key=self.api_key)
            assistant_message = await client.aio.models.generate_content(
                model= "gemini-2.0-flash-001",
                contents=formatted_messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type= "application/json",
                    response_schema= AIResponse,
                    max_output_tokens=4096,
                    temperature=temperature
                )
            )
            logger.info(f"Gemini API 원본 응답: {assistant_message}")
            return {"message": assistant_message.text}
        except Exception as e:
            logger.error(f"Gemini API 오류: {str(e)}")
            raise Exception(f"Gemini API 오류: {str(e)}")

    def agent_role(self, type: AttendeeType) -> str:
        return "model" if type == AttendeeType.bot else "user"
    
class ThirdPartyAIRequest:
    def __init__(self, prompt_context: PromptContext):
        self.prompt_context = prompt_context

    async def chat(self, recent_messages: List[Message], ai_model: str, temperature: float = 0.7) -> str:
        if "gpt" in ai_model:
            service = OpenAIRequest(ai_model)
        elif "claude" in ai_model:
            service = ClaudeRequest(ai_model)
        elif "gemini" in ai_model:
            service = GeminiRequest(ai_model)
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
