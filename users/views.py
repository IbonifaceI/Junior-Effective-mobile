from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
import os
from datetime import datetime, timedelta
from django.conf import settings

from .models import User, Role, BusinessElement, AccessRule
from .serializers import UserSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            password = request.data.get('password')
            if password:
                user.set_password(password)
                user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email, is_active=True)
            if user.check_password(password):
                # Генерируем токен на 1 час с id пользователя внутри
                token_data = {
                    'user_id': user.id,
                    'exp': datetime.utcnow() + timedelta(hours=1),
                    'iat': datetime.utcnow()
                }
                token = jwt.encode(token_data, settings.SECRET_KEY, algorithm='HS256')
                return Response({'token': token}, status=status.HTTP_200_OK)
            return Response({'error': 'Неверный пароль'}, status=status.HTTP_401_UNAUTHORIZED)
            
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)