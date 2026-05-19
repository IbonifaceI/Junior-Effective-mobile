import jwt
import os
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None # Нет заголовка, пропускаем (вернет 401 позже)
        
        try:
            # Bearer <token>
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                return None
            
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            if user_id is None:
                raise AuthenticationFailed('Invalid token payload')
                
            try:
                user = User.objects.get(id=user_id, is_active=True)
                return (user, None) # Возвращаем пользователя и None (как в стандарте DRF)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found or inactive')
                
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise AuthenticationFailed('Token is invalid or expired')