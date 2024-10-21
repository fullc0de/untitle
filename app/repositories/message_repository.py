from sqlmodel import Session, select
from app.models.message import Message, SenderType
from typing import List, Optional

class MessageRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_message(self, text: str, sender_type: SenderType) -> Message:
        message = Message(text=text, sender_type=sender_type)
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        return self.session.get(Message, message_id)

    def get_all_messages(self) -> List[Message]:
        return self.session.exec(select(Message)).all()

    def update_message(self, message_id: int, text: str) -> Optional[Message]:
        message = self.get_message_by_id(message_id)
        if message:
            message.text = text
            self.session.commit()
            self.session.refresh(message)
        return message

    def delete_message(self, message_id: int) -> bool:
        message = self.get_message_by_id(message_id)
        if message:
            self.session.delete(message)
            self.session.commit()
            return True
        return False

