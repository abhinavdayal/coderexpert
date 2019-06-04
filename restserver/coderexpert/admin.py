from django.contrib import admin

# Register your models here.
from .models import CodingProfile, Question, Attempt

admin.site.register(CodingProfile)
admin.site.register(Question)
admin.site.register(Attempt)