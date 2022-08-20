from django.forms import ValidationError
from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
        def create(self, validated_data):
            user = User.objects.create(**validated_data)
            return user
        
        def validate(self, attrs):
            email = attrs.get('email')
            username = attrs.get('username')
            
            if not email:
                raise ValidationError('Email is required')
            if not username:
                raise ValidationError('Username is required')
            return attrs

        
class LoginSerializer(serializers.ModelSerializer):
   password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    
   class Meta:
        model = User
        fields = ('email', 'password')

       
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']