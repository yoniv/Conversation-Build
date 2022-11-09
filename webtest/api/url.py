from django.contrib import admin
from django.urls import path
from.views import main

urlpatterns = [
    path('chats/<str:chat_id>/', main)
]
