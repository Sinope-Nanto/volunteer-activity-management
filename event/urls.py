from django.urls import path
from .views import CreateEventView, CreateProgramView, JoinEventView, QuitEventView, FinishEventView, DonorView, ChangeStatusView\
    , SearchProgramOrEventView, GetTargetInfoView, GetAllProgramInfoView, GetAllEventInfoView

urlpatterns = [
    path("newevent/", CreateEventView.as_view()),
    path("newprogram/", CreateProgramView.as_view()),
    path("join/", JoinEventView.as_view()),
    path("quit/", QuitEventView.as_view()),
    path("finish/", FinishEventView.as_view()),
    path("donor/", DonorView.as_view()),
    path("status/", ChangeStatusView.as_view()),
    path("getinfo/", GetTargetInfoView.as_view()),
    path("search/", SearchProgramOrEventView.as_view()),
    path("allprogram/", GetAllProgramInfoView.as_view()),
    path("allevent/", GetAllEventInfoView.as_view()),
]