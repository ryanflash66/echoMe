from django.urls import path
from . import views

urlpatterns = [
    path('tribes/', views.TribeListCreate.as_view(), name='tribe-list'),
    path('tribes/<int:pk>/', views.TribeDetail.as_view(), name='tribe-detail')
]