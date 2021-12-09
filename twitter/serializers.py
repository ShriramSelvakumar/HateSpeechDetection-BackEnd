from rest_framework import serializers
from .models import Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'user_code', 'user_session', 'consumer_key', 'consumer_secret',
                  'access_token', 'access_token_secret', 'created_at')


class CreateUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('consumer_key', 'consumer_secret', 'access_token', 'access_token_secret')
