from .models import lesson, Lesson, CourseAttempt, LessonAttempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

class CourseAttemptHelper:
    @staticmethod
    def create_course_attempt(course, user):
        course_attempt, created = CourseAttempt.objects.get_or_create(course=course, user=user)
        if created:
            course.attempt_count += 1
            course.save()
        else:
            CourseAttemptHelper.sync_course_attempt(course_attempt)
        return course_attempt

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
           course_attempt.update_time = datetime.now()
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

    @staticmethod
    def process_attempt(course_attempt, attempt, scorechange, first_attempt):
        course_attempt.latest_attempt_time = attempt.end_time
        if lesson_attempt.questions_completed == lesson.question_count:
            course_attempt.lessons_completed += 1
        
        course_attempt.score += scorechange
        course_attempt.save()


class LessonAttemptHelper:

    @staticmethod
    def create_lesson_attempt(lesson, user):
        lesson_attempt, created = LessonAttempt.objects.get_or_create(lesson=lesson, user=user)
        if created:
            courseattempt = CourseAttempt.objects.filter(course=lesson.course, user=request.user)
            courseattempt.lessonAttempts += 1
            courseattempt.save()
            lesson.attempt_count += 1
            lesson.save()
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
           lesson_attempt.update_time = datetime.now()
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

    @staticmethod
    def process_attempt(lesson_attempt, attempt, scorechange, first_attempt):
        lesson_attempt.latest_attempt_time = attempt.end_time
        if first_attempt:
            lesson_attempt.questions_completed += 1
        lesson_attempt.score += scorechange
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
    def process_attempt(attempt, scorechange):
        question = attempt.question
        question.total_score += scorechange
        question.total_attempts += 1
        question.last_attempt_time = datetime.now()
        if attempt.verdict == 'C':
            question.corrent_attempts += 1
        elif attempt.verdict == 'MLE':
            question.mle_attempts += 1
        elif attempt.verdict == 'TLE':
            question.tle_attempts += 1
        else:
            question.wrong_attempts += 1

        question.save()

class ProfileHelper:
    @staticmethod
    def process_attempt(attempt, scorechange, first_attempt):
        profile = attempt.user.coding_profile
        profile.total_score += scorechange
        profile.total_attempts += 1
        profile.last_active = datetime.now()
        profile.problems_solved += 1 if first_attempt else 0
        profile.save()
        
        
class GroupHelper:
    @staticmethod
    def process_attempt(attempt, scorechange, first_attempt):
         #find groups user belongs to and update the stats
        groups = GroupMember.objects.filter(user=attempt.user)
        for group in groups:
            if first_attempt:
                group.attempts += 1
            group.score += scorechange
            group.save()


class AttemptHelper:
    @staticmethod
    def update_attempt_stats(attempt):
        best_attempt = Attempt.objects.filter(question=attempt.question, user=attempt.user).aggregate(Max('score'), Max('end_time'))
        first_attempt = best_attempt == None and attempt.score > 0 and attempt.verdict=='C'
        scorechange = 0
        if first_attempt:
            scorechange = attempt.score
        elif best_attempt != None and attempt.score > best_attempt.score__max:
            scorechange = attempt.score - best_attempt.score__max

        ProfileHelper.process_attempt(attempt, scorechange, first_attempt)
        QuestionHelper.process_attempt(attempt, scorechange)
        GroupHelper.process_attempt(attempt, scorechange, first_attempt)

        # this question can be in multiple lessons
        lessons = LessonQuestion.objects.filter(question=attempt.question)
        for lesson in lessons:
            lesson_attempt = LessonAttempt.objects.get(lesson=lesson, user=attempt.user)
            LessonAttemptHelper.process_attempt(lesson_attempt, attempt, scorechange, first_attempt)

            course_attempt = CourseAttempt.objects.get(user=attempt.user, course=lesson.course)
            CourseAttemptHelper.process_attempt(attempt, scorechange, first_attempt)
            
            
           

            
            