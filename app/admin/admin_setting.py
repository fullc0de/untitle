from sqladmin import Admin, ModelView
from app.models import Message, MsgEmbedding, User, Bot, Session, Attendee
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

class SessionAdmin(ModelView, model=Session):
    column_list = [Session.id, Session.property, Session.created_at, Session.updated_at]
    column_sortable_list = [Session.id, Session.property]
    column_searchable_list = [Session.property]

def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(MessageAdmin)
    admin.add_view(MsgEmbeddingAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(BotAdmin)
    admin.add_view(SessionAdmin)
    return admin 
