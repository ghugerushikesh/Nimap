from rest_framework import serializers
from .models import User, Client, Project
from django.contrib.auth.hashers import make_password

class User_S(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'phone_number', 'address', 'location_city', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return super().create(validated_data)

class Client_S(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']  

class Project_S(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users']