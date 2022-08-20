from django.urls import path
from .views import *

app_name = 'user'


urlpatterns = [
    path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('chat', CreateChat.as_view(), name='chat'),
    path('chat/<int:sender>/<int:receiver>', CreateChat.as_view(), name='chat'),
]