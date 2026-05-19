from rest_framework import serializers
from .models import User, Role, BusinessElement, AccessRule

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True) # Пароль не будет возвращаться в ответе

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'is_active', 'password_hash']