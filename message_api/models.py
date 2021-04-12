from django.db import models

class Message(models.Model):
    sender = models.CharField(max_length = 200, default = "")
    receiver = models.CharField(max_length = 200, default = "")
    message = models.CharField(max_length = 1500, default = "")
    subject = models.CharField(max_length = 300, default = "")
    creation_date = models.DateTimeField(default = "")
    unread = models.BooleanField(default=True)

class LoggedInUsers(models.Model):
    user = models.CharField(max_length = 200)
    token = models.CharField(max_length = 200)
    login_date = models.DateTimeField(default = "")
