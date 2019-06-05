from .models import lesson, Lesson, CourseAttempt, LessonAttempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class CourseAttemptHelper:
    @staticmethod
    def get_user_course_attempt(course, user):
        course_attempt = None
        try:
            course_attempt = CourseAttempt.objects.get(course=course, user=user)
            CourseAttemptHelper.sync_course_attempt(course_attempt)
        except ObjectDoesNotExist:
            pass
        return course_attempt
    

    @staticmethod
    def get_all_user_course_attempts(user):
        course_attempts = CourseAttempt.objects.filter(user=user)
        for course_attempt in course_attempts:
            CourseAttemptHelper.sync_course_attempt(course_attempt)
        return course_attempts


    @staticmethod
    def sync_course_attempt(course_attempt):
        if not course_attempt.is_synced:
           lessonattempts = LessonAttempt.objects.filter(user=course_attempt.user, lesson__course=course_attempt.course)
           course_attempt.lesson_attempts = 0
           course_attempt.lessons_completed = 0
           course_attempt.score = 0
           course_attempt.latest_attempt_time = None
           for lessonattempt in lessonattempts:
               if not lessonattempt.is_synced:
                   LessonAttemptHelper.sync_lesson_attempt(lessonattempt)
               course_attempt.lesson_attempts += 1 if lessonattempt.questions_completed>0 else 0
               if lessonattempt.questions_completed==lessonattempt.lesson.question_count:
                   course_attempt.lessons_completed += 1 
               course_attempt.score += lessonattempt.score
               course_attempt.latest_attempt_time = lessonattempt.latest_attempt_time if course_attempt.latest_attempt_time==None else max(course_attempt.latest_attempt_time, lessonattempt.latest_attempt_time)
            course_attempt.save()

class LessonAttemptHelper:

    @staticmethod
    def create_lesson_attempt(lesson, user):
        lesson_attempt, created = LessonAttempt.objects.get_or_create(lesson=lesson, user=user)
        if created:
            courseattempt = CourseAttempt.objects.filter(course=lesson.course, user=request.user)
            courseattempt.lessonAttempts += 1
            courseattempt.save()
        else:
            LessonAttemptHelper.sync_lesson_attempt(lesson_attempt)
        return lesson_attempt
    
    @staticmethod
    def get_user_lesson_attempt(lesson, user):
        lesson_attempt = None
        try:
            lesson_attempt = LessonAttempt.objects.get(lesson=lesson, user=user)
            LessonAttemptHelper.sync_lesson_attempt(lesson_attempt)
        except ObjectDoesNotExist:
            pass
        return lesson_attempt

    @staticmethod
    def get_all_user_lesson_attempts(user, course):
        lesson_attempts = LessonAttempt.objects.filter(user=user, lesson__course=course)
        for lesson_attempt in lesson_attempts:
            LessonAttemptHelper.sync_lesson_attempt(lesson_attempt)
        return lesson_attempts

    @staticmethod
    def sync_lesson_attempt(lesson_attempt):
        if not lesson_attempt.is_synced:
           lesson_attempt.score = 0
           lesson_attempt.questions_completed = 0
           lesson_attempt.latest_attempt_time = None

           questions = LessonQuestion.objects.filter(lesson=lesson_attempt.lesson)
           
           for question in questions:
               attempt = Attempt.objects.filter(question=question.question, user=lesson_attempt.user).aggregate(Max('score'), Max('end_time'))
               if attempt != None:
                   lesson_attempt.questions_completed += 1 if attempt.score__max>0 else 0
                   lesson_attempt.score += attempt.score__max
                   lesson_attempt.latest_attempt_time = attempt.end_time__max if lesson_attempt.latest_attempt_time==None else max(lesson_attempt.latest_attempt_time, attempt.end_time__max)
           lesson_attempt.save()


class LessonHelper:
    @staticmethod
    def process_question_change(lesson, question_change):
        course = lesson.course

        lesson.question_count += question_change
        lesson.update_time = datetime.datetime.now()
        course.update_time = datetime.datetime.now()

        lesson.save()
        course.save()

class QuestionHelper:
    @staticmethod
    def create_question():
        pass