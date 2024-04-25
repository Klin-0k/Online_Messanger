from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="home"),
    path("auth", views.auth, name="auth"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("logout", LogoutView.as_view(next_page="auth"), name="logout"),
    path("<str:UserName>/friends", views.friends, name="friends"),
    path("<str:UserName>/messages", views.messages, name="messages"),
    path("<str:UserName>/profile", views.profile, name="profile"),
    path("<str:UserName>", views.index, name="home"),
    path("<str:UserName>/messages/<str:ChatName>", views.messages, name="messages"),
]
