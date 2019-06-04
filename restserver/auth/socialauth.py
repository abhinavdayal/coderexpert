from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
import json
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.permissions import AllowAny
from .models import College, Profile

class GoogleAuthentication(authentication.BaseAuthentication):
    permission_classes = (AllowAny,)
    def authenticate(self, request):
        if request.method!='POST':
            return None

        received_json_data=json.loads(request.body)
        user = None
        print(received_json_data["provider"])
        if received_json_data and received_json_data["provider"] =='GOOGLE':
            user = self.googleauth(received_json_data["idtoken"])
            if(user==None):
                raise exceptions.AuthenticationFailed("No such user")
        
        return (user,None)

    def googleauth(self, token):
        try:
            #print(token)
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), '3440031025-0ibqq9u77l693gj0ahrf815a86kt5cts.apps.googleusercontent.com')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            #print(idinfo['hd']) #check for the hosteddomain

            user = None

            try:
                #print("getting user")
                user = User.objects.get(username=idinfo['email'])
            except Exception as e:
                #print(e)
                #print("User not found")
                user = User.objects.create(username=idinfo['email'], email=idinfo['email'], first_name=idinfo['given_name'], last_name=idinfo['family_name'])
                profile = Profile.objects.get(pk=user.id)
                profile.provider = "GOOGLE"
                profile.save()

            return user
        except Exception as e:
            #print("Someo other error", e)
            return None