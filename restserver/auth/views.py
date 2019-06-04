from django.shortcuts import render
import json
from .serializers import CollegeSerializer, ProfileSerializer, StudyFieldSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import exception_handler
from rest_framework.permissions import IsAuthenticated, AllowAny

#model imports
from django.contrib.auth.models import User
from .models import College, Profile, StudyField

class ListCollegeView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    permission_classes = (IsAuthenticated,)
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

class ListStudyFieldView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = StudyField.objects.all()
    serializer_class = StudyFieldSerializer      

class JWTAuthentication(APIView):
    permission_classes = (AllowAny,)
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        if request.user == None:
            return Response({"error":"Unauthorized"}, 403)
        else:
            return Response(self.get_tokens_for_user(request.user))

    