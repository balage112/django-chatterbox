"""chatterbox_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import chatterbox.views

urlpatterns = [
    path('admin/', admin.site.urls),

    # chatterbox aplikace
    # path(<cesta>, <view> , name="name")
    path('', chatterbox.views.home, name='home'),
    path('hello/', chatterbox.views.hello),
    path('hello/<s>', chatterbox.views.hello),
    path('search/<s>', chatterbox.views.search, name="search"),
    path('room/<str:pk>/', chatterbox.views.room, name="room"),
    path('rooms/', chatterbox.views.rooms, name="rooms"),
    path('delete_room/<str:pk>/', chatterbox.views.delete_room, name="delete_room"),
    path("edit_room/<pk>/", chatterbox.views.EditRoom.as_view(), name="edit_room"),

    # accounts aplikace
    path("accounts/", include("accounts.urls")), # vytvoří pouze signup
    path("accounts/", include("django.contrib.auth.urls")), # vytvoří zbytek - login, logout, password_change atd...

    path("__reload__/", include("django_browser_reload.urls")), # automatický reload stránky
    path('create_room/', chatterbox.views.create_room, name="create_room"),


]
