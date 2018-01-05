from django.db import models


class User(models.Model):
    social_id = models.CharField(max_length=64, unique=True)
    access_token = models.CharField(max_length=256, unique=True)
    expire_dt = models.DateTimeField()
    create_dt = models.DateTimeField(auto_now_add=True)
    modify_dt = models.DateTimeField(auto_now=True)
