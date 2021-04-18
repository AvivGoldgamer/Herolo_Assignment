"""Home_Assignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from message_api.views import sendMessage, getMessages, getUnreadMessages, readMessage, deleteMessage, login, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sendmsg/', sendMessage),
    path("getmsg/", getMessages),
    path("getunreadmsg/", getUnreadMessages),
    path("readmsg/", readMessage),
    path("delmsg/", deleteMessage),
    path("login/", login),
    path("register/", register)
]
