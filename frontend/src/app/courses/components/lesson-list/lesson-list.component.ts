import { Component, OnInit, Input } from '@angular/core';
import { Lesson, LessonAttempt, Course } from '../../models/models';

@Component({
   selector: 'app-lesson-list',
   templateUrl: './lesson-list.component.html',
   styleUrls: ['./lesson-list.component.scss']
})
export class LessonListComponent implements OnInit {

   @Input() lessons: Array<Lesson> = [];
   @Input() from = 0;
   @Input() to = 10;
   @Input() search = '';
   @Input() display = 0;
   @Input() lessonattempts: Array<LessonAttempt> = [];
   @Input() subscribed = false;
   @Input() course: Course;


   constructor() { }

   getlessonattempt(l: Lesson): LessonAttempt {
      let a: LessonAttempt = null;
      if (this.lessonattempts) { a = this.lessonattempts.find(x => x.lesson === l.id); }
      a = a || new LessonAttempt(l.id);
      return a;
   }

   FilteredLessons(): Array<Lesson> {
      return this.lessons.filter
         (lesson => {
            return (this.search === '' || lesson.title.toLowerCase().includes(this.search.toLowerCase()));
         });
      // TODO: handle display
   }

   ngOnInit() {
   }

}
