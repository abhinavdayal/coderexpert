from django.db import models
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
from django.contrib.auth.models import User

import .services

# Create your models here.
class CodingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    geeks_handle = models.CharField(max_length=30, null=True)
    hackerrank_handle = models.CharField(max_length=30, null=True)
    interviewbit_handle = models.CharField(max_length=30, null=True)
    codechef_handle = models.CharField(max_length=30, null=True)
    codeforces_handle = models.CharField(max_length=30, null=True)
    problems_solved = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    last_active = models.DateTimeField(auto_now_add=True)
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user

@receiver(post_save, sender=User)
def create_user_coding_profile(sender, instance, created, **kwargs):
    if created:
        CodingProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_coding_profile(sender, instance, **kwargs):
    instance.coding_profile.save()

class Course(models.Model):
   title = models.CharField(max_length=50)
   description = models.CharField(max_length=1000)
   image = models.URLField(max_length=200, blank=True)
   lesson_count = models.IntegerField(default=0)
   update_time = models.DateTimeField(auto_now_add=True)
   attempt_count = models.IntegerField(default=0)
   def __str__(self):
        return self.title

   class Meta:
        ordering = ('title',)


class CourseAttempt(models.Model):
   course = models.ForeignKey(Course, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   start_time = models.DateTimeField(auto_now_add=True)
   latest_attempt_time = models.DateTimeField(blank=True, null=True)
   update_time = models.DateTimeField(auto_now_add=True)
   # below 3 feels must be calculated fields if underlying course is updated
   # after the last update time, but then we need to update the last update time also
   lessons_completed = models.IntegerField(default=0)
   lesson_attempts = models.IntegerField(default=0)
   score = models.IntegerField(default=0)
   #TODO: create internal fields that can store stale data, but the access is through propery methods
   @property
   def is_synced(self):
       return self.update_time > self.course.update_time


class Lesson(models.Model):
   title = models.CharField(max_length=50)
   description = models.CharField(max_length=1000)
   course = models.ForeignKey(Course)
   image = models.URLField(max_length=200, blank=True)
   question_count = models.IntegerField(default=0)
   update_time = models.DateTimeField(auto_now_add=True)
   content = models.TextField(blank=True)
   attempt_count = models.IntegerField(default=0)

   def __str__(self):
        return self.title

   class Meta:
        ordering = ('title',)

@receiver(pre_delete, sender=Lesson)
def delete_lesson(sender, instance, **kwargs):
      instance.course.lesson_count -= 1
      instance.course.update_time = datetime.datetime.now()
      instance.course.save()
      

class LessonAttempt(models.Model):
   lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   start_time = models.DateTimeField(auto_now_add=True)
   latest_attempt_time = models.DateTimeField(blank=True, null=True)
   update_time = models.DateTimeField(auto_now_add=True)
   questions_completed = models.IntegerField(default=0)
   score = models.IntegerField(default=0)

   @property
   def is_synced(self):
       return self.update_time > self.lesson.update_time
       

class Group(models.Model):
    title = models.CharField(max_length=50, db_index=True)
    description = models.CharField(max_length=500)
    score = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)

class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Tag(models.Model):
    topic = models.CharField(max_length=50)

    def __str__(self):
        return self.topic

class Question(models.Model):
    DOMAINS = (
        ('GFG', 'geeksforgeeks.org'),
        ('HR', 'hackerrank.com'),
        ('IB', 'interviewbit.com'),
        ('CC', 'codechef.com'),
        ('CF', 'codeforces.com'),
    )
    title = models.CharField(max_length=50, db_index=True)
    question = models.TextField()
    content = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    score = models.IntegerField(max_length=3)
    url = models.URLField(max_length=256, unique=True)
    level = models.IntegerField(max_length=1, validators=[MaxValueValidator(5), MinValueValidator(1)], default=3)
    domain = models.CharField(max_length=3, choices=DOMAINS)
    qid = models.CharField(max_length=20)
    accuracy = models.FloatField()

    total_attempts = model.IntegerField(default=0)
    correct_attempts = models.IntegerField(default=0)
    tle_attempts = models.IntegerField(default=0)
    wrong_attempts = models.IntegerField(default=0)
    mle_attempts = models.IntegerField(default=0)
    last_attempt_time = models.DateTimeField(blank=True)

    @property
    def local_accuracy(self):
       return self.correct_attempts/self.total_attempts if self.total_attempts>0 else 0


    total_score = models.IntegerField(default=0)
    #we have to store and update a lots of analytics, so we need to think over how to do that in a manageable and efficient manner


    def __str__(self):
        return self.url

class UserQuestionView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    view_time = models.DateTimeField(auto_now_add=True)

class Attempt(models.Model):
    VERDICTS = (
        ('NA', 'Not Attempted')
        ('C', 'Correct'),
        ('W', 'Wrong'),
        ('TLE', 'Time Limit Exceeded'),
        ('MLE', 'Memory Limit Exceeded'),
    )
    LANGUAGES = (
        ('C', 'C'),
        ('CPP', 'C++'),
        ('JAVA', 'JAVA'),
        ('PYTHON', 'PYTHON'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=3, choices=VERDICTS, default='NA')
    answer = models.TextField(blank=True) 
    language = models.CharField(max_length=10, choices=LANGUAGES, blank=True)
    attempt_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)


    def __str__(self):
        return '%s - %s' % (self.user.email, self.question.url)

@receiver(pre_save, sender=Attempt)
def save_user_attempt(sender, instance, **kwargs):
    services.AttemptHelper.update_attempt_stats(instance)


class LessonQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # can record attempts done via this lesson separately
    # how to settle a question linked to multiple lessons, if user completes it
    # should all lessons be updated? Then many to many pmapping will be more effective
    # A LessonQestion can be deleted but it does not impact the questionfrontend
    # When you add a question, you search for question or put URL and create
    # Upon deletion of lessonQuestion, its stats in lesson is changed, and all lesson_attempts must change
    # But this only impacts the current lesson and not other lessons.
    # a scrape of attempts also looks into existig attempts, so we need not worry about updating on the fly
    # however deletion need to be updated

@receiver(pre_delete, sender=LessonQuestion)
def delete_lesson_question(sender, instance, **kwargs):
      services.LessonHelper.process_question_change(instance.lesson, -1)
      
@receiver(pre_save, sender=LessonQuestion)
def create_lesson_question(sender, instance, **kwargs):
      services.LessonHelper.process_question_change(instance.lesson, 1)
    

        






