from rest_framework import serializers
from .models import CodingProfile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodingProfile
        fields = "__all__"

