from rest_framework import serializers
from .models import Tribe, User

class TribeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tribe
        fields = ['id','name','creator','created_at']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'friends', 'tribes']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user