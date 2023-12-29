from django.urls import path
from .views import login_view, signup_view,chat_word

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', signup_view, name='signup'),
    path('chat_word/', chat_word, name='chat_word'),
]

