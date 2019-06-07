from rest_framework import serializers
from .models import CodingProfile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodingProfile
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
   class Meta:
        model = Course
        fields = '__all__'

class CourseIdSerializer(serializers.ModelSerializer):
   class Meta:
        model = Course
        fields = ("id",)

class LessonSerializer(serializers.ModelSerializer):
   class Meta:
        model = Lesson
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
   class Meta:
        model = Question
        fields = ('id', 'title', 'score', 'level', 'accuracy', 'local_accuracy')

class QuestionDetailsSerializer(serializers.ModelSerializer):
   class Meta:
        model = Question
        fields = '__all__'

class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'question', 'content', 'score', 'url', 'level', 'domain', 'qid', 'accuracy')

class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'description', 'image')

class CreateLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'description', 'content', 'image', 'course')

class LessonAttemptSerializer(serializers.ModelSerializer):
   class Meta:
        model = LessonAttempt
        fields = '__all__'

class CourseAttemptSerializer(serializers.ModelSerializer):
   class Meta:
        model = CourseAttempt
        fields = '__all__'

class AttemptSerializer(serializers.Serializer):
   question = serializers.IntegerField()
   count = serializers.IntegerField()
   bestscore = serializers.IntegerField()
   totalscore = serializers.IntegerField()

