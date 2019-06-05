from .models import lesson, Lesson, CourseAttempt, LessonAttempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class SyncCourseAttempt:
    @staticmethod
    def get_user_course_attempt(course, user):
        course_attempt = None
        try:
            course_attempt = CourseAttempt.objects.get(course=course, user=user)
            course_attempt.sync()
        except ObjectDoesNotExist:
            pass
        return course_attempt
    

    @staticmethod
    def get_all_user_course_attempts(user):
        course_attempts = CourseAttempt.objects.filter(user=user)
        for course_attempt in course_attempts:
            course_attempt.sync()
        return course_attempts
    
    @staticmethod
    def get_user_lesson_attempt(lesson, user):
        lesson_attempt = None
        try:
            lesson_attempt = LessonAttempt.objects.get(lesson=lesson, user=user)
            lesson_attempt.sync()
        except ObjectDoesNotExist:
            pass
        return lesson_attempt

    @staticmethod
    def get_all_user_lesson_attempts(user, course):
        lesson_attempts = LessonAttempt.objects.filter(user=user, lesson__course=course)
        for lesson_attempt in lesson_attempts:
            lesson_attempt.sync()
        return lesson_attempts