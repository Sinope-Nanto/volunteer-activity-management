from django.urls import path
from .views import CreateEventView, CreateProgramView

urlpatterns = [
    path("newevent/", CreateEventView.as_view()),
    path("newprogram/", CreateProgramView.as_view()),
]