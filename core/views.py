import csv
from django.shortcuts import render
from django.db.models import F
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from core import serializers, models
from django.http import HttpResponse


User = get_user_model()

class CreateUserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, created = Token.objects.get_or_create(user_id=response.data["id"])
        response.data["share_url"] = f'http://frontend.com/{str(token)}'
        
        user = models.UserToken(user_id=response.data['id'], token=token)
        user.save()
        
        score = models.Score(user_id=response.data['id'], score=1)
        score.save()

        if not request.data.get('token') == None:
            token = models.UserToken.objects.filter(token=request.data['token'])
            if token:
                models.Score.objects.filter(user_id=token[0].user.id).update(score=F('score') + 1)
            else:
                return Response({'error': 'Token not found'})
        return response

class UserTokenView(viewsets.ModelViewSet):
    queryset = models.UserToken.objects.all()
    serializer_class = serializers.UserTokenSerializer

class ScoreView(viewsets.ModelViewSet):
    queryset = models.Score.objects.order_by('-score').all()[:10]
    serializer_class = serializers.ScoreSerializer

class ExportWinnersToCsv(APIView):
    def get(self, request):
        output = []
        response = HttpResponse(content_type='text/csv')
        writer = csv.writer(response)
        query_set = models.Score.objects.order_by('-score').all()[:10]
        writer.writerow(['user', 'score'])
        for user in query_set:
            output.append([user.user, user.score])
        writer.writerows(output)
        return response