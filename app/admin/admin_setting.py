from sqladmin import Admin, ModelView
from app.models.message import Message
from app.models.msg_embedding import MsgEmbedding

class MessageAdmin(ModelView, model=Message):
    column_list = [Message.id, Message.text]
    column_sortable_list = [Message.id, Message.text]
    column_searchable_list = [Message.text]

class MsgEmbeddingAdmin(ModelView, model=MsgEmbedding):
    column_list = [MsgEmbedding.id, MsgEmbedding.message_id]
    column_sortable_list = [MsgEmbedding.id, MsgEmbedding.message_id]
    column_searchable_list = [MsgEmbedding.message_id]

def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(MessageAdmin)
    admin.add_view(MsgEmbeddingAdmin)
    return admin 
