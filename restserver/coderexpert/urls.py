from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='fetch_profile'),
    path('getquestiondetails/', views.QuestionDetailsView.as_view(), name='fetch_question_details'),
]
