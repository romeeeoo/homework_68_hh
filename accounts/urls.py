from django.urls import path

from accounts.views import RegisterView, LoginView, ProfileView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("account/<int:pk>/", ProfileView.as_view(), name="account")
]
