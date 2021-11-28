from django.urls import path
from .views import LoginView, RegisterView, PermissionManageView, UserStatusManageView, ChangePasswordView, ChangeUserProflieView

urlpatterns = [
   path("login/", LoginView.as_view()),
   path("register/", RegisterView.as_view()),
   path("permission/", PermissionManageView.as_view()),
   path("status/", UserStatusManageView.as_view()),
   path("changepassword/", ChangePasswordView.as_view()),
   path('changeinformation/', ChangeUserProflieView.as_view()),
]
