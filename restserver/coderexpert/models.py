from django.db import models
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
from django.contrib.auth.models import User

# Create your models here.
class CodingProfile(model.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    geeks_handle = models.CharField(max_length=30, null=True)
    hackerrank_handle = models.CharField(max_length=30, null=True)
    interviewbit_handle = models.CharField(max_length=30, null=True)
    codechef_handle = models.CharField(max_length=30, null=True)
    codeforces_handle = models.CharField(max_length=30, null=True)

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
   def __str__(self):
        return self.title

   class Meta:
        ordering = ('title',)


class CourseAttempt(models.Model):
   course = models.ForeignKey(Course, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   start_time = models.DateTimeField(auto_now_add=True)
   completion_time = models.DateTimeField(blank=True, null=True)
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

   def sync(self):
       if not self.is_synced:
           # queries to update this courseattempt
           # get all lesson attempts
           # check if they are synced
           lessonattempts = LessonAttempt.objects.filter(user=self.user, lesson__course=self.course)
           self.lesson_attempts = 0
           self.lessons_completed = 0
           self.score = 0
           self.completion_time = None
           latest_completion_time = None
           for lessonattempt in lessonattempts:
               if not lessonattempt.is_synced:
                   lessonattempt.sync()
               self.lesson_attempts += 1 if lessonattempt.questions_completed>0 else 0
               if lessonattempt.questions_completed==lessonattempt.lesson.question_count:
                   self.lessons_completed += 1 
                   latest_completion_time = lessonattempt.completion_time
               self.score += lessonattempt.score
            if self.lessons_completed == self.course.lesson_count:
                self.completion_time = latest_completion_time
            self.save()



class Lesson(models.Model):
   title = models.CharField(max_length=50)
   description = models.CharField(max_length=1000)
   course = models.ForeignKey(Course)
   image = models.URLField(max_length=200, blank=True)
   question_count = models.IntegerField(default=0)
   update_time = models.DateTimeField(auto_now_add=True)

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
   completion_time = models.DateTimeField(blank=True, null=True)
   update_time = models.DateTimeField(auto_now_add=True)
   questions_completed = models.IntegerField(default=0)
   score = models.IntegerField(default=0)

   @property
   def is_synced(self):
       return self.update_time > self.lesson.update_time

   def sync(self):
       if not self.is_synced:
           # queries to update this courseattempt
           # get all lesson attempts
           # check if they are synced
           latest_attempt_time = None
           self.score = 0
           self.questions_completed = 0
           self.completion_time = None

           questions = LessonQuestion.objects.filter(lesson=self)
           
           for question in questions:
               attempt = Attempt.objects.filter(question=question.question, user=self.user).aggregate(Max('score'), Max('end_time'))
               if attempt != None:
                   self.questions_completed += 1 if attempt.score__max>0 else 0
                   self.score += attempt.score__max
                   latest_attempt_time = attempt.end_time__max
           if self.questions_completed == self.lesson.question_count:
               self.completion_time = latest_attempt_time
           self.save()

class LessonQuestion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # can record attempts done via this lesson separately
    # how to settle a question linked to multiple lessons, if user completes it
    # should all lessons be updated? Then many to many pmapping will be more effective
    # A LessonQestion can be deleted but it does not impact the question
    # When you add a question, you search for question or put URL and create
    # Upon deletion of lessonQuestion, its stats in lesson is changed, and all lesson_attempts must change
    # But this only impacts the current lesson and not other lessons.
    # a scrape of attempts also looks into existig attempts, so we need not worry about updating on the fly
    # however deletion need to be updated

@receiver(pre_delete, sender=LessonQuestion)
def delete_lesson_question(sender, instance, **kwargs):
      instance.lesson.question_count -= 1
      instance.lesson.update_time = datetime.datetime.now()
      instance.lesson.save()
      
@receiver(pre_save, sender=LessonQuestion)
def create_lesson_question(sender, instance, **kwargs):
      instance.lesson.question_count += 1
      instance.lesson.update_time = datetime.datetime.now()
      instance.lesson.save()


class Tag(model.Model):
    topic = models.CharField(max_length=50)

    def __str__(self):
        return self.topic

class Question(model.Model):
    DOMAINS = (
        ('GFG', 'geeksforgeeks.org'),
        ('HR', 'hackerrank.com'),
        ('IB', 'interviewbit.com'),
        ('CC', 'codechef.com'),
        ('CF', 'codeforces.com'),
    )
    title = models.CharField(max_length=50, db_index=True)
    question = models.TextField()
    tags = models.ManyToManyField(Tag)
    score = models.IntegerField(max_length=3)
    url = models.URLField(max_length=256, unique=True)
    level = models.IntegerField(max_length=1, validators=[MaxValueValidator(5), MinValueValidator(1)], default=3)
    domain = models.CharField(max_length=3, choices=DOMAINS)
    qid = models.CharField(max_length=20)
    accuracy = models.FloatField()

    def __str__(self):
        return self.url

class Attempt(model.Model):
    VERDICTS = (
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
    verdict = models.CharField(max_length=3, choices=VERDICTS)
    answer = models.TextField() 
    language = models.CharField(max_length=10, choices=LANGUAGES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    minutes_taken = models.IntegerField()
    score = models.IntegerField()

    def __str__(self):
        return '%s - %s' % (self.user.email, self.question.url)






