from django.shortcuts import render
import json
import .scraper
from .serializers import CodingProfileSerializer
from auth.serializers import ProfileSerializer
from rest_framework.response import Response

# Create your views here.
# Create your views here.
class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        profile = Profile.objects.get(pk=request.user.id)
        try:
            codingprofile = CodingProfile.objects.get(pk=request.user.id)
        except Exception as e:
            print(e)

        return Response({'profile': ProfileSerializer(profile).data, 'codingprofile': CodingProfileSerializer(codingprofile).data})

    def post(self, request):
        try:
            profile = Profile.objects.get(pk=request.user.id)
            codingprofile = CodingProfile.objects.get(pk=request.user.id)
            profile.savedata(request.data["profile"])
            codingprofile.savedata(request.data["codingprofile"])
            return Response(request.data, status=201)
        except:
            return Response(request.data, status=400)

class QuestionDetailsView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(Self, request):
        try:
            url = request.data["url"]
            domain = request.data["domain"]
            #scrape the url here 
            if domain=='GFG':
                return Response(scraper.getGeeksForGeeksQuestionDetail(url))
            else:
                raise ValueError('Unsupported Domain: '+domain)
        except Exception as e:
            return Response({"error":str(e)}, status=400)