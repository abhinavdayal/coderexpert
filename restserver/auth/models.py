from django.db import models
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
from django.contrib.auth.models import User

class College(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class StudyField(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.OneToOneField(College, on_delete=models.SET_NULL, null=True)
    fieldofstudy = models.OneToOneField(StudyField, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=10, null=True)
    YEAR_CHOICES = []
    for r in range((datetime.datetime.now().year), (datetime.datetime.now().year+5)):
        YEAR_CHOICES.append((r,r))

    graduation_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    provider = models.CharField(max_length=20, null=True)

    def savedata(self, data):
        self.graduation_year = data["graduation_year"]
        self.phone = data["phone"]
        self.filedofstudy = StudyField.objects.get(pk=data["fieldofstudy"])
        self.college = College.objects.get(pk=data["college"])
        self.save()

    def __str__(self):
        return '%s %s' % (self.college.name, self.fieldofstudy.name)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


