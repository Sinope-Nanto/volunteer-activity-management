from django.urls import path
from .views import CreateEventView, CreateProgramView, JoinEventView, QuitEventView

urlpatterns = [
    path("newevent/", CreateEventView.as_view()),
    path("newprogram/", CreateProgramView.as_view()),
    path("join/", JoinEventView.as_view()),
    path("quit/", QuitEventView.as_view()),
]