from typing import Optional
from app.models import FactSnapshot
import app.prompts as prompts

class PromptContext:
    chat_prompt_template = ""
    summary_prompt_template = ""

    def build(self, fact_snapshot: Optional[FactSnapshot]) -> None:
        if fact_snapshot is None:
            self.chat_prompt_template = self.chat_prompt_template.format(character_info="없음", conversation_summary="없음")
            # self.summary_prompt_template = self.summary_prompt_template.format(current_summary="없음")
            return

        interest_keywords = fact_snapshot.character_info.get("interest_keywords", [])
        expertise_keywords = fact_snapshot.character_info.get("expertise_keywords", [])
        
        # 리스트가 아닌 경우 빈 리스트로 변환
        if not isinstance(interest_keywords, list):
            interest_keywords = []
        if not isinstance(expertise_keywords, list):
            expertise_keywords = []

        c_info = {
            "이름": fact_snapshot.character_info.get("name", ""),
            "성별": fact_snapshot.character_info.get("gender", ""),
            "관계": fact_snapshot.character_info.get("relationship", ""),
            "관심사 키워드": ", ".join(interest_keywords),
            "전문분야 키워드": ", ".join(expertise_keywords)
        }
        self.chat_prompt_template = self.chat_prompt_template.format(
            character_info=c_info,
            conversation_summary=fact_snapshot.conversation_summary
        )
        # self.summary_prompt_template = self.summary_prompt_template.format(
        #     current_summary=fact_snapshot.conversation_summary
        # )