from django.urls import path
from submission import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('leaderboard/', views.Leaderboard.as_view(), name='leaderboard'),
]
