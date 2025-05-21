from abc import ABC, abstractmethod
import json
import os
from dotenv import load_dotenv
from typing import Dict, List, Any
import logging
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from google import genai
from google.genai import types
from app.models import Chat, FactSnapshot
from app.models.chat import SenderType
from app.requests.prompt_context import PromptContext
from app.requests.ai_resp_scheme import CharacterJsonResponse, SummaryResponse

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIRequest(ABC):
    @abstractmethod
    async def chat(self, system_prompt: str, messages: List[Chat], temperature: float) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def summary(self, system_prompt: str, request: str, temperature: float) -> Dict[str, Any]:
        pass

    @abstractmethod
    def agent_role(self, is_bot: bool) -> str:
        pass

    @abstractmethod
    def build_message(self, chat: Chat) -> str:
        pass

class OpenRouterRequest(AIRequest):
    def __init__(self, model: str):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"

    async def chat(self, system_prompt: str, chats: List[Chat], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            {"role": "system", "content": system_prompt},
            *[
                types.Content(
                    role=self.agent_role(chat.sender_type == SenderType.bot),
                    parts=[types.Part.from_text(text=self.build_message(chat))]
                ) 
                for chat in chats
            ]
        ]

        try:
            logger.info(f"OpenRouter API 요청: 최근 메시지 갯수: {len(formatted_messages)}")
            logger.info(f"OpenRouter API 요청: formatted_messages: {formatted_messages}")
            async with AsyncOpenAI(api_key=self.api_key, base_url=self.base_url) as client:
                response = await client.chat.completions.create(
                    max_tokens=8192,
                    messages=formatted_messages,
                    model="google/gemini-2.0-flash-001",
                    temperature=temperature,
                    response_format=CharacterJsonResponse.json_schema(),
                )
                content = response.choices[0].message.content
                logger.info(f"OpenRouter API 응답 원본: {content}")
                
                return {"message": content}
                    
        except Exception as e:
            logger.error(f"OpenRouter API 오류: {str(e)}")
            raise Exception(f"OpenRouter API 오류: {str(e)}")

    async def summary(self, system_prompt: str, request: str, temperature: float) -> Dict[str, Any]:
        raise NotImplementedError("OpenRouter API는 summary 기능을 지원하지 않습니다.")

    def agent_role(self, is_bot: bool) -> str:
        return "assistant" if is_bot else "user"
    
    def build_message(self, chat: Chat) -> str:
        return chat.content["text"]
    
class OpenAIRequest(AIRequest):
    def __init__(self, model: str):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model

    async def chat(self, system_prompt: str, chats: List[Chat], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            {"role": "system", "content": system_prompt},
            *[
                types.Content(
                    role=self.agent_role(chat.sender_type == SenderType.bot),
                    parts=[types.Part.from_text(text=self.build_message(chat))]
                ) 
                for chat in chats
            ]
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
                    response_format=CharacterJsonResponse
                )
            logger.info(f"OpenAI API 원본 응답: {assistant_message}")
            return {"message": assistant_message.choices[0].message.content}
        except Exception as e:
            logger.error(f"OpenAI API 오류: {str(e)}")
            raise Exception(f"OpenAI API 오류: {str(e)}")

    async def summary(self, system_prompt: str, request: str, temperature: float) -> Dict[str, Any]:
        raise NotImplementedError("OpenAI API는 summary 기능을 지원하지 않습니다.")

    def agent_role(self, is_bot: bool) -> str:
        return "assistant" if is_bot else "user"

    def build_message(self, chat: Chat) -> str:
        return chat.content["text"]
    
class ClaudeRequest(AIRequest):
    def __init__(self, model: str):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        
    async def chat(self, system_prompt: str, chats: List[Chat], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            *[
                types.Content(
                    role=self.agent_role(chat.sender_type == SenderType.bot),
                    parts=[types.Part.from_text(text=self.build_message(chat))]
                ) 
                for chat in chats
            ]
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
        
    async def summary(self, system_prompt: str, request: str, temperature: float) -> Dict[str, Any]:
        raise NotImplementedError("Claude API는 summary 기능을 지원하지 않습니다.")

    def agent_role(self, is_bot: bool) -> str:
        return "assistant" if is_bot else "user"

    def build_message(self, chat: Chat) -> str:
        return chat.content["text"]

class GeminiRequest(AIRequest):
    def __init__(self, model: str):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = model

    async def chat(self, system_prompt: str, chats: List[Chat], temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            *[
                types.Content(
                    role=self.agent_role(chat.sender_type == SenderType.bot),
                    parts=[types.Part.from_text(text=self.build_message(chat))]
                ) 
                for chat in chats
            ]
        ]

        try:
            logger.info(f"Gemini API 요청: 최근 메시지 갯수: {len(formatted_messages)}")
            logger.info(f"Gemini API 요청: formatted_messages: {formatted_messages}")
            client = genai.Client(api_key=self.api_key)
            assistant_message = await client.aio.models.generate_content(
                #model= "gemini-2.0-flash",
                model= "gemini-2.5-flash-preview-05-20",
                contents=formatted_messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type= "application/json",
                    response_schema= CharacterJsonResponse,
                    max_output_tokens=4092,
                    temperature=temperature
                )
            )
            logger.info(f"Gemini API 원본 응답: {assistant_message}")
            logger.info(f"프롬프트 토큰 수: {assistant_message.usage_metadata.prompt_token_count}")
            logger.info(f"Output 토큰 수: {assistant_message.usage_metadata.candidates_token_count}")
            logger.info(f"총 토큰 수: {assistant_message.usage_metadata.total_token_count}")

            return {"message": assistant_message.text}
        except Exception as e:
            logger.error(f"Gemini API 오류: {str(e)}")
            raise Exception(f"Gemini API 오류: {str(e)}")

    async def summary(self, system_prompt: str, request: str, temperature: float) -> Dict[str, Any]:
        formatted_messages = [
            types.Content(role="user", parts=[types.Part.from_text(text=request)])
        ]
        try:
            logger.info(f"Gemini Completion API 요청: formatted_messages: {formatted_messages}")
            client = genai.Client(api_key=self.api_key)
            assistant_message = await client.aio.models.generate_content(
                model= "gemini-2.0-flash-lite",
                contents=formatted_messages,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=temperature,
                        response_mime_type= "application/json",
                        response_schema= SummaryResponse
                    )
                )
            logger.info(f"Gemini 요약 원본 응답: {assistant_message}")
            logger.info(f"프롬프트 요약 토큰 수: {assistant_message.usage_metadata.prompt_token_count}")
            logger.info(f"Output 요약 토큰 수: {assistant_message.usage_metadata.candidates_token_count}")
            logger.info(f"총 요약 토큰 수: {assistant_message.usage_metadata.total_token_count}")

            return assistant_message.text
        except Exception as e:
            logger.error(f"Gemini Completion API 오류: {str(e)}")
            raise Exception(f"Gemini Completion API 오류: {str(e)}")

    def agent_role(self, is_bot: bool) -> str:
        return "model" if is_bot else "user"
    
    def build_message(self, chat: Chat) -> str:
        if chat.sender_type == SenderType.bot:
            return chat.content["text"]
        else:
            timestamp = int(chat.created_at.timestamp())
            temp = {
                "message": chat.content["text"],
                "created_timestamp": timestamp
            }
            return json.dumps(temp)
    
class ThirdPartyAIRequest:
    def __init__(self, prompt_context: PromptContext):
        self.prompt_context = prompt_context

    def get_request(self, model: str) -> AIRequest:
        if "gpt" in model:
            return OpenAIRequest(model)
        elif "claude" in model:
            return ClaudeRequest(model)
        elif "gemini" in model:
            return GeminiRequest(model)
        elif "openrouter" in model:
            return OpenRouterRequest(model)
        else:
            raise ValueError(f"지원하지 않는 AI 모델입니다: {model}")

    async def chat(self, recent_messages: List[Chat], ai_model: str, temperature: float = 0.7) -> str:
        service = self.get_request(ai_model)
        response = await service.chat(self.prompt_context.chat_prompt_template, recent_messages, temperature)
        return response['message']
        
    async def summary(self, ai_model: str, request: str, temperature: float) -> str:
        service = self.get_request(ai_model)
        response = await service.summary(self.prompt_context.summary_prompt_template, request, temperature)
        return response

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
