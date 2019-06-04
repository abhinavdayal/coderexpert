from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('colleges/', views.ListCollegeView.as_view(), name='list_colleges'),
    path('studyfields/', views.ListStudyFieldView.as_view(), name='fetch_study_fields'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', views.JWTAuthentication.as_view(), name='token_obtain_pair'),
]
