from sqladmin import Admin, ModelView
from app.models import Chat, MsgEmbedding, User, Bot, Chatroom
import json

class ChatAdmin(ModelView, model=Chat):
    column_list = [Chat.id, Chat.content, Chat.created_at, Chat.updated_at]
    column_sortable_list = [Chat.id, Chat.created_at, Chat.updated_at]
    column_searchable_list = [Chat.content]

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.nickname, User.profile, User.created_at, User.updated_at]
    column_sortable_list = [User.id, User.nickname, User.created_at, User.updated_at]
    column_searchable_list = [User.nickname]

class BotAdmin(ModelView, model=Bot):
    column_list = [Bot.id, Bot.name, Bot.profile, Bot.created_at, Bot.updated_at]
    column_sortable_list = [Bot.id, Bot.name]
    column_searchable_list = [Bot.name]
    form_columns = [Bot.name, Bot.profile]

class ChatroomAdmin(ModelView, model=Chatroom):
    column_list = [Chatroom.id, Chatroom.property, Chatroom.created_at, Chatroom.updated_at]
    column_sortable_list = [Chatroom.id, Chatroom.property]
    column_searchable_list = [Chatroom.property]

def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(ChatAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(BotAdmin)
    admin.add_view(ChatroomAdmin)
    return admin 
