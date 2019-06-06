from django.shortcuts import render
import json
from . import scraper
from . import services
from .serializers import CodingProfileSerializer, \
    CourseSerializer, CourseIdSerializer, LessonSerializer, QuestionSerializer, \
    CourseAttemptSerializer, LessonAttemptSerializer, AttemptSerializer

from auth.serializers import ProfileSerializer
from rest_framework.response import Response

from .models import CodingProfile, Course, Lesson, Question, Attempt, CourseAttempt, LessonAttempt, LessonQuestion, Group, GroupMember

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

"""
get question details of an online question vial web scraping
"""
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

"""
Get lessons in a course only if user has subscribed to that course
"""
class ListGetLessonsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LessonSerializer

    def get_queryset(self):
       courseid = self.kwargs['courseid']
       user = self.request.user

       subscribedcourse = Course.objects.get(pk=courseid)
       # we dont need to sync here. 
       ca = CourseAttempt.objects.get(user=self.request.user, course=subscribedcourse)
       if ca:
         return Lesson.objects.filter(courses=subscribedcourse)

"""
Get a particular course and course attempt for a user, given courseid and username
"""
class CourseView(APIView):
   permission_classes = (IsAuthenticated,)

   def get(self, request):
      courseid = self.kwargs['courseid']
      subscribedcourse = Course.objects.get(pk=courseid)
      courseattempt = services.CourseAttemptHelper.get_user_course_attempt(subscribedcourse, request.user)
      return Response({'course': CourseSerializer(subscribedcourse).data, 'attempt': CourseAttemptSerializer(courseattempt).data})


"""
Get all lesson attempts of a user for a given subscribed course
"""
class ListGetLessonAttemptsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LessonAttemptSerializer

    def get_queryset(self):
       courseid = self.kwargs['courseid']
       user = self.request.user

       subscribedcourse = Course.objects.get(pk=courseid)
       ca = CourseAttempt.objects.get(user=self.request.user, course=subscribedcourse)
       if ca:
         return services.LessonAttemptHelper.get_all_user_lesson_attempts(request.user, subscribedcourse)


"""
Get all questions inside a lesson only if lesson belongs to a course that is subscribed by the user
"""
class ListGetQuestionsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer

    def get_queryset(self):
       courseid = self.kwargs['courseid']
       lessonid = self.kwargs['lessonid']
       if courseid:
         subscribedcourse = Course.objects.get(pk=courseid)
         #no need to sync here
         ca = CourseAttempt.objects.get(user=self.request.user, course=subscribedcourse)
         if ca and lessonid:
            lesson = Lesson.objects.get(pk=lessonid)
            return Question.objects.filter(lesson=lesson)

"""
Get summary of attempts made for all questions in a lesson that belongs to a subscribed course
"""
class ListGetAttemptsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AttemptSerializer

    def get_queryset(self):
       courseid = self.kwargs['courseid']
       lessonid = self.kwargs['lessonid']
       if courseid:
         subscribedcourse = Course.objects.get(pk=courseid)
         # no need to sync here
         ca = CourseAttempt.objects.get(user=self.request.user, course=subscribedcourse)
         if ca and lessonid:
            lesson = Lesson.objects.get(pk=lessonid)
            questions = LessonQuestion.objects.filter(lesson=lesson)
            return Attempt.objects.filter(user=self.request.user, question__in=questions).annotate(bestscore=Max('score'), count=Count('id'), totalscore=Sum('score'))

"""
Get all courses in the system for an authorized user
"""
class ListCoursesView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

"""
Get all subscribed courses for which user has made attempts
"""
class ListSubscribedCoursesView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseAttemptSerializer
    def get_queryset(self):
       return services.CourseAttemptHelper.get_all_user_course_attempts(self.request.user)

"""
User can Subscribe to a course by creating a CourseAttempt object
"""
class SubscribeCourseView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            course = Course.objects.get(pk=request.data["courseid"])
            c = services.CourseAttemptHelper.create_course_attempt(course, request.user)
            return Response(CourseAttemptSerializer(c).data, status=201)
        except Exception as e:
            print(e)
            return Response(request.data, status=400)

"""
Get course info and the courseattempt infor for a subscribed course for a user
"""
class SubscribedCourseView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, courseid):
        try:
            course = Course.objects.get(pk=courseid)
            c = services.CourseAttemptHelper.get_user_course_attempt(course, request.user)
            return Response({'course': CourseSerializer(course).data, 'attempt':CourseAttemptSerializer(c).data}, status=201)
        except Exception as e:
            return Response({'error':e}, status=400)

"""
Get the lesson and its attempt for a user when lesson belongs to a subscribed course
Create an attempt if its the first time he clicked on the lesson
"""
class SubscribedLessonView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, lessonid):
        try:
            lesson = Lesson.objects.get(pk=lessonid)
            ca = CourseAttempt.objects.get(user=request.user, course=lesson.course)
            if ca:
                l = services.LessonAttemptHelper.create_lesson_attempt(lesson, request.user)
                return Response({'lesson': LessonSerializer(lesson).data, 'attempt':LessonAttemptSerializer(l).data}, status=201)
            else:
                raise ValueError('you are not subscribed to this course')
        except Exception as e:
            print(e)
            return Response({'error':e}, status=400)

"""
Create a course
"""
class CreateCourseView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            #profile.savedata(request.data["profile"])
            #codingprofile.savedata(request.data["codingprofile"])
            #create course from post data
            return Response(request.data, status=201)
        except:
            return Response(request.data, status=400)