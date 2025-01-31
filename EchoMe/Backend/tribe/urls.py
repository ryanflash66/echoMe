from django.urls import path
from . import views

urlpatterns = [
    path('tribes/', views.TribeListCreate.as_view(), name='tribe-list'),
    path('tribes/<int:pk>/', views.TribeDetail.as_view(), name='tribe-detail'),
    path('users/', views.UserCreate.as_view(), name='user-create'),
    path('users/<str:username>/', views.UserDetail.as_view(), name='user-detail'),
]