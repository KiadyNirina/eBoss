from typing import Any, Dict
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from .models import *

class CustomUserSerializer(serializers.ModelSerializer) :
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only = True)
    groups = serializers.PrimaryKeyRelatedField(many = True, queryset = Group.objects.all())
    user_permissions = serializers.PrimaryKeyRelatedField(many = True, queryset = Permission.objects.all())

    class Meta :
        model = CustomUser
        fields = '__all__'
    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        permissios_data = validated_data.pop('user_permissions', [])
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        if password != confirm_password :
            raise serializers.ValidationError({"password": "Password fields didin't match."})
        user = CustomUser.objects.create(**validated_data)
            # email = validated_data['email'],
            # username = validated_data['username'],
            # password = validated_data['password'],
            # role = validated_data.get('role', 'school')
        user.set_password(password)
        user.save()

        user.groups.set(groups_data)
        user.user_permissions.set(permissios_data)

        return user


class StudentListSerializer(serializers.ModelSerializer) :
    class Meta :
        model = CustomUser
        fields = '__all__'

class MatiereListSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Matiere
        fields = '__all__'

class InfoFamilialeSerializer(serializers.ModelSerializer) :
    class Meta :
        model = InfoFamiliale
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Course
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Schedule
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Note
        fields = '__all__'

class RegistrationDataSerializer(serializers.ModelSerializer) :
    class Meta :
        model = RegistrationData
        fields = '__all__'