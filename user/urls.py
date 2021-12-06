from django.urls import path
from .views import LoginView, RegisterView, PermissionManageView, UserStatusManageView, ChangePasswordView, ChangeUserProflieView, SearchUserView, GetUserProflieView, GetAllUserProfileView

urlpatterns = [
   path("login/", LoginView.as_view()),
   path("register/", RegisterView.as_view()),
   path("permission/", PermissionManageView.as_view()),
   path("status/", UserStatusManageView.as_view()),
   path("changepassword/", ChangePasswordView.as_view()),
   path('changeinformation/', ChangeUserProflieView.as_view()),
   path('search/', SearchUserView.as_view()),
   path('getuser/', GetUserProflieView.as_view()),
   path('getalluser/', GetAllUserProfileView.as_view()),
]
