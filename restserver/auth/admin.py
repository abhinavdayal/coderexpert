from django.contrib import admin

# Register your models here.
from .models import College, Profile, StudyField

admin.site.register(College)
admin.site.register(StudyField)
admin.site.register(Profile)