from django.shortcuts import render
from rest_framework import generics 
from .models import Tribe
from .serializers import TribeSerializer

class TribeListCreate(generics.ListCreateAPIView):
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer
class TribeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer


