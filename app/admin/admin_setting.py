from sqladmin import Admin, ModelView
from app.models import Message, MsgEmbedding, User, Bot, Chatroom, Attendee, UserPersona, AttendeesRelationship
import json

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
    form_columns = [Bot.name, Bot.ai_model, Bot.property]

class ChatroomAdmin(ModelView, model=Chatroom):
    column_list = [Chatroom.id, Chatroom.property, Chatroom.created_at, Chatroom.updated_at]
    column_sortable_list = [Chatroom.id, Chatroom.property]
    column_searchable_list = [Chatroom.property]

class AttendeeAdmin(ModelView, model=Attendee):
    column_list = [Attendee.id, Attendee.chatroom_id, Attendee.target_id, Attendee.attendee_type]
    column_sortable_list = [Attendee.id]
    column_searchable_list = [Attendee.chatroom_id, Attendee.target_id]

class UserPersonaAdmin(ModelView, model=UserPersona):
    column_list = [UserPersona.id, UserPersona.user_id, UserPersona.attendee_id, UserPersona.chatroom_id, UserPersona.nickname, UserPersona.age, UserPersona.gender, UserPersona.description]
    column_sortable_list = [UserPersona.id, UserPersona.user_id, UserPersona.attendee_id, UserPersona.chatroom_id, UserPersona.nickname, UserPersona.age, UserPersona.gender]
    column_searchable_list = [UserPersona.nickname, UserPersona.user_id]

class AttendeesRelationshipAdmin(ModelView, model=AttendeesRelationship):
    column_list = [AttendeesRelationship.id, AttendeesRelationship.chatroom_id, AttendeesRelationship.relationship]
    column_sortable_list = [AttendeesRelationship.id, AttendeesRelationship.chatroom_id]
    column_searchable_list = [AttendeesRelationship.relationship]

def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(MessageAdmin)
    admin.add_view(MsgEmbeddingAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(BotAdmin)
    admin.add_view(ChatroomAdmin)
    admin.add_view(AttendeeAdmin)
    admin.add_view(UserPersonaAdmin)
    admin.add_view(AttendeesRelationshipAdmin)
    return admin 
