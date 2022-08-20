from rest_framework import generics, status
from .serializers import *
from .models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser

# Create your views here.
class Register(generics.GenericAPIView):
    permissions_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    
    """Endpoint to register other users"""
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = make_password(serializer.validated_data['password'])
            try:    
                user = User.objects.create(username=username, email=email, password=password)
                user.save()
                return Response({"success": f"{username} successfully created"}, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error":str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permissions_classes = [permissions.AllowAny]
    
    """Endpoint to login a user"""
    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        if email is None or password is None:
            return Response(data={'invalid_credentials': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=email, password=password)
        if not user:
            return Response(data={'invalid_credentials': 'Ensure both email and password are correct'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'token': token.key}, status=status.HTTP_200_OK)
    
    
class CreateChat(generics.GenericAPIView):
    serializer_class = MessageSerializer
    
    def get(self, request, sender=None, receiver=None):
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post (self, request):
        data = JSONParser().parse(request)
        serializer = self.serializer_class(data=data) 
        if serializer.is_valid():
            serializer.save()   
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400) 
                