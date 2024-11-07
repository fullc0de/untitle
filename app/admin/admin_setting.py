from sqladmin import Admin, ModelView
from app.models import Message, MsgEmbedding, User, Bot, Chatroom, Attendee
class MessageAdmin(ModelView, model=Message):
    column_list = [Message.id, Message.text]
    column_sortable_list = [Message.id, Message.text]
    column_searchable_list = [Message.text]

class MsgEmbeddingAdmin(ModelView, model=MsgEmbedding):
    column_list = [MsgEmbedding.id, MsgEmbedding.message_id]
    column_sortable_list = [MsgEmbedding.id, MsgEmbedding.message_id]
    column_searchable_list = [MsgEmbedding.message_id]

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.nickname, User.role, User.created_at, User.updated_at]
    column_sortable_list = [User.id, User.nickname, User.created_at, User.updated_at]
    column_searchable_list = [User.nickname]

class BotAdmin(ModelView, model=Bot):
    column_list = [Bot.id, Bot.name, Bot.ai_model, Bot.property]
    column_sortable_list = [Bot.id, Bot.name]
    column_searchable_list = [Bot.name, Bot.ai_model]

class ChatroomAdmin(ModelView, model=Chatroom):
    column_list = [Chatroom.id, Chatroom.property, Chatroom.created_at, Chatroom.updated_at]
    column_sortable_list = [Chatroom.id, Chatroom.property]
    column_searchable_list = [Chatroom.property]

def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(MessageAdmin)
    admin.add_view(MsgEmbeddingAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(BotAdmin)
    admin.add_view(ChatroomAdmin)
    return admin 
