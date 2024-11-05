from sqlmodel import Session, select, delete
from app.models.message import Message, SenderType
from app.models.msg_embedding import MsgEmbedding
from typing import List, Optional, Dict
from sqlalchemy import ARRAY
import numpy as np

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

    def delete_all_messages(self):
        self.session.exec(delete(Message))
        self.session.commit()

    def get_latest_messages(self, limit: int) -> List[Message]:
        return self.session.exec(
            select(Message)
            .order_by(Message.id.desc())
            .limit(limit)
        ).all()

################################################################################
# for msg_embedding
################################################################################

    def create_embedding(self, embedding: List[float], message_id: int) -> MsgEmbedding:
        chat_embedding = MsgEmbedding(embedding=embedding, message_id=message_id)
        self.session.add(chat_embedding)
        self.session.commit()
        self.session.refresh(chat_embedding)
        return chat_embedding

    def create_embeddings(self, embeddings: Dict[int, List[float]]) -> List[MsgEmbedding]:
        chat_embeddings = [MsgEmbedding(embedding=embedding, message_id=message_id) for message_id, embedding in embeddings.items()]
        self.session.add_all(chat_embeddings)
        self.session.commit()
        created_embeddings = self.session.exec(select(MsgEmbedding).where(MsgEmbedding.message_id.in_(embeddings.keys()))).all()
        return created_embeddings

    def delete_all_embeddings(self):
        self.session.exec(delete(MsgEmbedding))
        self.session.commit()

    def get_embedding_by_id(self, embedding_id: int) -> Optional[MsgEmbedding]:
        return self.session.get(MsgEmbedding, embedding_id)

    def get_embedding_by_message_id(self, message_id: int) -> Optional[MsgEmbedding]:
        return self.session.exec(select(MsgEmbedding).where(MsgEmbedding.message_id == message_id)).first()

    def get_all_embeddings(self) -> List[MsgEmbedding]:
        return self.session.exec(select(MsgEmbedding)).all()

    def update_embedding(self, embedding_id: int, new_embedding: List[float]) -> Optional[MsgEmbedding]:
        chat_embedding = self.get_embedding_by_id(embedding_id)
        if chat_embedding:
            chat_embedding.embedding = new_embedding
            self.session.commit()
            self.session.refresh(chat_embedding)
        return chat_embedding

    def delete_embedding(self, embedding_id: int) -> bool:
        chat_embedding = self.get_embedding_by_id(embedding_id)
        if chat_embedding:
            self.session.delete(chat_embedding)
            self.session.commit()
            return True
        return False

    def find_similar_embeddings(self, query_embedding: List[float], limit: int = 5) -> List[MsgEmbedding]:
        all_embeddings = self.get_all_embeddings()
        similarities = []
        for embedding in all_embeddings:
            similarity = self.cosine_similarity(query_embedding, embedding.embedding)
            similarities.append((embedding, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in similarities[:limit]]

    @staticmethod
    def cosine_similarity(a: List[float], b: List[float]) -> float:
        a_np = np.array(a)
        b_np = np.array(b)
        return np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np))