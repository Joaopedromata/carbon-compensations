from django.contrib import admin
from django.urls import path, include
from core import models, views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('create_user', views.CreateUserView, basename='Users')
router.register('user_token', views.UserTokenView, basename='Tokens')
router.register('score', views.ScoreView, basename='Scores')

urlpatterns = [
    *router.urls,
    path('winners/', views.ExportWinnersToCsv.as_view()) 
]
