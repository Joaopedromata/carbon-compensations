from rest_framework import serializers
from django.contrib.auth import get_user_model
from core import models

User = get_user_model()

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserToken
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'phone_number'
        ]

class UserName(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class ScoreSerializer(serializers.ModelSerializer):

    user = UserName()

    class Meta: 
        model = models.Score
        fields = ['user', 'score']