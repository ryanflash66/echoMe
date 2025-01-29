from rest_framework import serializers
from .models import Tribe

class TribeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tribe
        fields = ['id','name','creator','created_at']