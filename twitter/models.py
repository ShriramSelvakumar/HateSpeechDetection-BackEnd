from django.db import models
import string
import random


def generate_unique_code():
    length = 8

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Users.objects.filter(user_code=code).count() == 0:
            break

    return code


class Users(models.Model):
    user_code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    user_session = models.CharField(max_length=50, unique=True)
    consumer_key = models.CharField(max_length=75, null=False)
    consumer_secret = models.CharField(max_length=75, null=False)
    access_token = models.CharField(max_length=75, null=False)
    access_token_secret = models.CharField(max_length=75, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
