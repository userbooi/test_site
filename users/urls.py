from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path('login-user/', views.login_user, name="login_user"),
    path("logout-user/", views.logout_user, name="logout_user"),
    path("register/", views.register, name="register")
]
