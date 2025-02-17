from django.urls import path
from . import views

urlpatterns = [
    path('tribes/', views.TribeListCreate.as_view(), name='tribe-list'),
    path('tribes/<int:pk>/', views.TribeDetail.as_view(), name='tribe-detail'),
    path('users/', views.UserCreate.as_view(), name='user-create'),
    path('users/<str:username>/', views.UserDetail.as_view(), name='user-detail'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
    path('users/<str:username>/playlists/', views.get_user_playlists, name='user-playlists'),
]