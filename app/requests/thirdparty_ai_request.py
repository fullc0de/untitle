from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Tuple, Optional
import logging
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from google import genai
from google.genai import types
from pydantic import BaseModel
from app.models import Chat
import app.prompts as prompts
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptContext:
    prompt_template = prompts.prompt_multiple_persona_template

    # ## 메시지 예시 ##
    # - *머리를 긁적이며 쑥스럽게 웃는다. 볼이 발그레해지며 고개를 살짝 숙인다.* 에헤헤... 방금 실수하나 했는데 혹시 뭔지 봤어?
    # - *소매 끝을 잡고 얼굴을 가리며 작게 웃는다. 살짝 떨리는 목소리로 말한다.* 나… 나 이렇게 가까이 있으면… 너무 떨려…

    def __init__(self, prompt_template: str = prompt_template):
        self.prompt_template = prompt_template

class AIRequest(ABC):
    @abstractmethod
    async def chat(self, system_prompt: str, messages: List[Chat], temperature: float) -> Dict[str, Any]:
        pass

    @abstractmethod
    def agent_role(self, is_bot: bool) -> str:
        pass

class CharacterResponse(BaseModel):
    name: str
    #attendee_id: Optional[int] = None
    is_main_character: bool
    is_storyteller: bool
    message: str

class AIResponse(BaseModel):
    messages: List[CharacterResponse]
    summary: str

class OpenRouterRequest(AIRequest):
    def __init__(self, model: str):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"

    async def chat(self, system_prompt: str, chats: List[Chat], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            {"role": "system", "content": system_prompt},
            *[{"role": self.agent_role(chat.sender_id), "content": chat.content} for chat in chats]
        ]

        try:
            logger.info(f"OpenRouter API 요청: 최근 메시지 갯수: {len(formatted_messages)}")
            logger.info(f"OpenRouter API 요청: formatted_messages: {formatted_messages}")
            async with AsyncOpenAI(api_key=self.api_key, base_url=self.base_url) as client:
                assistant_message = await client.beta.chat.completions.parse(
                    max_tokens=8192,
                    messages=formatted_messages,
                    model= "google/gemini-2.0-flash-001",
                    temperature=temperature,
                    response_format=AIResponse,
                    max_completion_tokens=2048
                )
            logger.info(f"OpenRouter API 원본 응답: {assistant_message}")
            return {"message": assistant_message.choices[0].message.content}
        except Exception as e:
            logger.error(f"OpenRouter API 오류: {str(e)}")
            raise Exception(f"OpenRouter API 오류: {str(e)}")

    def agent_role(self, is_bot: bool) -> str:
        return "assistant" if is_bot else "user"
    
class OpenAIRequest(AIRequest):
    def __init__(self, model: str):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model

    async def chat(self, system_prompt: str, chats: List[Chat], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            {"role": "system", "content": system_prompt},
            *[{"role": self.agent_role(chat.sender_id), "content": chat.content} for chat in chats]
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

    def agent_role(self, is_bot: bool) -> str:
        return "assistant" if is_bot else "user"

class ClaudeRequest(AIRequest):
    def __init__(self, model: str):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        
    async def chat(self, system_prompt: str, chats: List[Chat], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            *[{"role": self.agent_role(chat.sender_id), "content": chat.content} for chat in chats]
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
        
    def agent_role(self, is_bot: bool) -> str:
        return "assistant" if is_bot else "user"

class GeminiRequest(AIRequest):
    def __init__(self, model: str):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = model

    async def chat(self, system_prompt: str, chats: List[Chat], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            *[types.Content(role=self.agent_role(chat.sender_id), parts=[types.Part.from_text(text=chat.content)]) for chat in chats]
        ]

        try:
            logger.info(f"Gemini API 요청: 최근 메시지 갯수: {len(formatted_messages)}")
            logger.info(f"Gemini API 요청: formatted_messages: {formatted_messages}")
            client = genai.Client(api_key=self.api_key)
            assistant_message = await client.aio.models.generate_content(
                model= "gemini-2.0-flash",
                #model= "gemini-2.5-pro-exp-03-25",
                contents=formatted_messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type= "application/json",
                    response_schema= AIResponse,
                    max_output_tokens=8192 * 2,
                    temperature=temperature
                )
            )
            logger.info(f"Gemini API 원본 응답: {assistant_message}")

            token_count = await client.aio.models.count_tokens(
                model="gemini-2.0-flash",
                #model="gemini-2.5-pro-exp-03-25",
                contents=[
                    types.Content(
                        role="system",
                        parts=[types.Part.from_text(text=system_prompt)]
                    ),
                    *formatted_messages,
                    types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=assistant_message.text)]
                    )
                ]
            )
            logger.info(f"토큰 수: {token_count}")

            return {"message": assistant_message.text}
        except Exception as e:
            logger.error(f"Gemini API 오류: {str(e)}")
            raise Exception(f"Gemini API 오류: {str(e)}")

    def agent_role(self, is_bot: bool) -> str:
        return "model" if is_bot else "user"
    
class ThirdPartyAIRequest:
    def __init__(self, prompt_context: PromptContext):
        self.prompt_context = prompt_context

    async def chat(self, recent_messages: List[Chat], ai_model: str, temperature: float = 0.7) -> str:
        if "gpt" in ai_model:
            service = OpenAIRequest(ai_model)
        elif "claude" in ai_model:
            service = ClaudeRequest(ai_model)
        elif "gemini" in ai_model:
            service = GeminiRequest(ai_model)
        elif "openrouter" in ai_model:
            service = OpenRouterRequest(ai_model)
        else:
            raise ValueError(f"지원하지 않는 AI 모델입니다: {ai_model}")

        response = await service.chat(self.prompt_context.prompt_template, recent_messages, temperature)
        
        return response['message']
        

# class EmbeddingRequest:
#     def __init__(self, chat_repository: ChatRepository):
#         self.api_key = os.getenv("OPENAI_API_KEY")
#         self.model = "text-embedding-3-large"
#         self.chat_repository = chat_repository

#     async def create_msg_embedding(self, msg: str, msg_id: str) -> None:
#         try:
#             # request embeddings
#             async with AsyncOpenAI(api_key=self.api_key) as client:
#                 response = await client.embeddings.create(
#                     model=self.model,
#                     input=msg
#                 )

#             # store them into db
#             embedding_data = response.data[0].embedding
#             self.chat_repository.create_embedding(embedding_data, msg_id)
#             logger.info(f"Embedding has been successfully created: corresponding msg_id: {msg_id}")

#         except Exception as e:
#             logger.error(f"임베딩 생성 중 오류 발생: {str(e)}")

#     # (int, str) = (msg_id, msg)
#     async def create_msg_embedding_batch(self, messages: List[Tuple[int, str]]) -> None:
#         try:
#             async with AsyncOpenAI(api_key=self.api_key) as client:
#                 response = await client.embeddings.create(
#                     model=self.model,
#                     input=[item[1] for item in messages]
#                 )

#             embeddings = {}
#             for idx, item in enumerate(messages):
#                 embeddings[item[0]] = response.data[idx].embedding
#             self.chat_repository.create_embeddings(embeddings)
            
#         except Exception as e:
#             logger.error(f"임베딩 생성 (배치) 중 오류 발생: {str(e)}")
