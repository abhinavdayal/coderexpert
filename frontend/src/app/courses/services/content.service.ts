import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { config } from 'src/app/config';
import { Course, Lesson, CourseAttempt, LessonAttempt, Question, Attempt } from '../models/models';
import { Observable } from 'rxjs';

@Injectable({
   providedIn: 'root'
})
export class ContentService {

   constructor(private http: HttpClient) { }

   getCourse(courseid: number): Observable<any> {
      return this.http.get<any>(`${config.apiUrl}/coderexpert/getcourse/${courseid}/`);
   }

   getLesson(lessonid: number): Observable<any> {
      return this.http.get<any>(`${config.apiUrl}/coderexpert/getlesson/${lessonid}/`);
   }

   getCourses(): Observable<Array<Course>> {
      return this.http.get<Array<Course>>(`${config.apiUrl}/coderexpert/courses/`);
   }

   getMyCourses(): Observable<Array<CourseAttempt>> {
      return this.http.get<Array<CourseAttempt>>(`${config.apiUrl}/coderexpert/mycourses/`);
   }

   getLessonAttempts(courseid: number): Observable<Array<LessonAttempt>> {
      return this.http.get<Array<LessonAttempt>>(`${config.apiUrl}/coderexpert/lessonattempts/${courseid}/`);
   }

   getLessons(courseid: number): Observable<Array<Lesson>> {
      return this.http.get<Array<Lesson>>(`${config.apiUrl}/coderexpert/lessons/${courseid}/`);
   }

   getQuestions(courseid: number, lessonid: number): Observable<Array<Question>> {
      return this.http.get<Array<Question>>(`${config.apiUrl}/coderexpert/questions/${courseid}/${lessonid}/`);
   }

   getAttempts(courseid: number, lessonid: number): Observable<Array<Attempt>> {
      return this.http.get<Array<Attempt>>(`${config.apiUrl}/coderexpert/attempts/${courseid}/${lessonid}/`);
   }

   subscribeCourse(id: number): Observable<CourseAttempt> {
      return this.http.post<any>(`${config.apiUrl}/coderexpert/subscribecourse/`, {courseid: id});
   }
}
