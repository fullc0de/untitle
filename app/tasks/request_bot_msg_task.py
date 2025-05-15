from app.celery_app import app
from app.database import engine
from sqlmodel import Session
from typing import Dict
import logging
from dotenv import load_dotenv
import asyncio
import redis
import os
from app.models.chat import SenderType
from app.repositories.chat_repository import ChatRepository
from app.requests.thirdparty_ai_request import ThirdPartyAIRequest, PromptContext
from app.task_models.msg_info import MsgInfo
import app.prompts as prompts
# from app.helpers.prompt_builder import build_prompt
import json


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

@app.task
def request_bot_msg_task(chatroom_id: int, temperature=0.7) -> MsgInfo:
    async def async_chat():
        try:
            with Session(engine) as session:
                chat_repository = ChatRepository(session)

                chatroom = chat_repository.get_chatroom_by_id(chatroom_id)
                recent_messages = chat_repository.get_latest_messages(chatroom_id, 5)
                logger.info(f"recent_messages: {recent_messages.reverse()}")

                latest_fact_snapshot = chat_repository.get_latest_fact_snapshot(chatroom_id)

                prompt_context = PromptContext()
                prompt_context.chat_prompt_template = prompts.prompt_unknown_template_2
                prompt_context.summary_prompt_template = prompts.prompt_template_summary
                prompt_context.build(latest_fact_snapshot)
                logger.info(f"chat_prompt_template: {prompt_context.chat_prompt_template}")
                logger.info(f"summary_prompt_template: {prompt_context.summary_prompt_template}")

                ai_model = "gemini"

                ai_request = ThirdPartyAIRequest(prompt_context)
                ai_msg = await ai_request.chat(recent_messages, ai_model, temperature)
                logger.info(f"Bot 메시지: {ai_msg}")
                json_msg = json.loads(ai_msg)
                content = {
                    "text": json_msg["message"],
                    "original_response": json_msg
                }
                message = chat_repository.create_chat(content, chatroom_id, chatroom.bot.id, SenderType.bot)
                session.commit()
                session.refresh(message)
                
                # 새로운 fact_snapshot 생성
                new_fact = json_msg["character_facts"].get("newly_established_fact_on_both_user_and_character")
                if new_fact:
                    summary_response = await ai_request.summary(ai_model, new_fact, 0.5)
                    summary_dict = json.loads(summary_response)
                    logger.info(f"summary: {summary_dict}")
                    chat_repository.create_fact_snapshot(chatroom_id, message.id, summary_dict["chatbot_info"], summary_dict["facts_summary"])
                    session.commit()
                    session.refresh(message)

                # 메시지를 딕셔너리로 변환 후 JSON 직렬화
                message_json = message.model_dump_json()
                logger.info(f"serialized message: {message_json}")
                
                # web 서버로 메시지 전송 (web 서버가 클라이언트에게 전달함)
                message_dict = json.loads(message_json)
                message_dict['content']['original_response'] = None
                message_json = json.dumps(message_dict)
                redis_client.publish("chat_messages", message_json)
                
                # # 업데이트 facts
                # facts = message.content['original_response']['character_facts']
                # prompt_modifier = chatroom.get_prompt_modifier()
                # if facts['newly_discovered_facts'] != None:
                #     prompt_modifier.facts.append(facts['newly_discovered_facts'])
                # chatroom.set_prompt_modifier(prompt_modifier)
                # session.commit()
                # session.refresh(chatroom)

                return MsgInfo(msg=ai_msg, msg_id=message.id)
        except Exception as e:
            logger.error(f"Error in request_bot_msg_task: {str(e)}")
            return json.dumps({"error": str(e)})

    return asyncio.run(async_chat())
