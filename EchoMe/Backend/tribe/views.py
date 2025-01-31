from django.shortcuts import render
from rest_framework import generics 
from rest_framework.response import Response
from .models import Tribe , User
from .serializers import TribeSerializer , UserSerializer

class TribeListCreate(generics.ListCreateAPIView):
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer
class TribeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def retrieve(self, request, *args, **kwargs):
        try:
            print(f"Attempting to retrieve user with username: {kwargs.get('username')}")
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            print(f"Serialized data: {serializer.data}")
            return Response(serializer.data)
        except Exception as e:
            print(f"Error retrieving user: {str(e)}")
            raise


