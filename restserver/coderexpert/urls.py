from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='fetch_profile'),
    path('getquestiondetails/', views.QuestionDetailsView.as_view(), name='fetch_question_details'),
    path('courses/', views.ListCoursesView.as_view(), name='fetch_courses'),
    path('categories/', views.ListCategoriesView.as_view(), name='fetch_categories'),
    path('mycourses/', views.ListSubscribedCoursesView.as_view(), name='fetch_my_courses'),
    path('subscribecourse/', views.SubscribeCourseView.as_view(), name='subscribe_courses'),
    re_path(r'^getcourse/(?P<courseid>\d+)/$', views.SubscribedCourseView.as_view(), name='fetch_course_details'),
    re_path(r'^getlesson/(?P<lessonid>\d+)/$', views.SubscribedLessonView.as_view(), name='fetch_lesson_details'),
    re_path(r'^lessons/(?P<courseid>\d+)/$', views.ListGetLessonsView.as_view(), name='fetch_lessons_in_course'),
    re_path(r'^lessonattempts/(?P<courseid>\d+)/$', views.ListGetLessonAttemptsView.as_view(), name='fetch_lesson_attempts_in_course'),
    re_path(r'^questions/(?P<courseid>\d+)/(?P<lessonid>\d+)/$', views.ListGetQuestionsView.as_view(), name='fetch_questions_in_lesson'),
    re_path(r'^attempts/(?P<courseid>\d+)/(?P<lessonid>\d+)/$', views.ListGetAttemptsView.as_view(), name='fetch_attempt_summary_in_lesson'),
]
