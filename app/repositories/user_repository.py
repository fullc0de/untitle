from sqlmodel import Session, select
from app.models import User, Bot, UserPersona
from app.models.attendee import Attendee, AttendeeType
from typing import List

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.session.exec(stmt).first()

    def get_bot_by_id(self, bot_id: int) -> Bot | None:
        stmt = select(Bot).where(Bot.id == bot_id)
        return self.session.exec(stmt).first()
        
    def get_bot_by_attendee_id(self, attendee_id: int) -> Bot | None:
        stmt = select(Bot).join(Attendee, Attendee.target_id == Bot.id).where(Attendee.id == attendee_id)
        return self.session.exec(stmt).first()
    
    def get_user_by_attendee_id(self, attendee_id: int) -> User | None:
        stmt = select(User).join(Attendee, Attendee.target_id == User.id).where(Attendee.id == attendee_id)
        return self.session.exec(stmt).first()

    def get_attendees_by_user_id(self, user_id: int) -> List[Attendee]:
        stmt = select(Attendee).where(
            Attendee.target_id == user_id,
            Attendee.attendee_type == AttendeeType.user
        )
        return self.session.exec(stmt).all()

    def user_persona_by_attendee_id(self, attendee_id: int) -> UserPersona | None:
        stmt = select(UserPersona).where(UserPersona.attendee_id == attendee_id)
        return self.session.exec(stmt).first()
    
    def user_persona_by_user_id(self, user_id: int, chatroom_id: int) -> UserPersona | None:
        stmt = select(UserPersona).where(UserPersona.user_id == user_id, UserPersona.chatroom_id == chatroom_id)
        return self.session.exec(stmt).first()
