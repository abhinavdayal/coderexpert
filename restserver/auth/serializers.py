from rest_framework import serializers
from .models import College, Profile, StudyField
from django.contrib.auth.models import User

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ("id","name")

class StudyFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyField
        fields = ("id", "name")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("phone", "college","fieldofstudy","graduation_year")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ('url', 'username', 'email', 'groups')
        fields = ('username', 'first_name', 'last_name', 'email')