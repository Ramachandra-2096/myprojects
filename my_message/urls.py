from django.urls import path
from my_message.views import chat_view,custom_login,get_messages
urlpatterns = [
    path("",custom_login,name="custom_login"),
    path("chat",chat_view,name="chat"),
    path("get_messages",get_messages,name="get_messages"),
]
