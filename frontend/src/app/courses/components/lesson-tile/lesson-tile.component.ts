import { Component, OnInit, Input } from '@angular/core';
import { Lesson, LessonAttempt, Course } from '../../models/models';
import { config } from 'src/app/config';

@Component({
   selector: 'app-lesson-tile',
   templateUrl: './lesson-tile.component.html',
   styleUrls: ['./lesson-tile.component.scss']
})
export class LessonTileComponent implements OnInit {

   @Input() lesson: Lesson;
   @Input() lessonattempt: LessonAttempt;
   @Input() subscribed = false;
   @Input() course: Course;
   lessonImage: string;
   constructor() { }

   ngOnInit() {
      this.lessonImage = this.lesson.image;
      if (!this.lesson.image || this.lesson.image === '') { this.lessonImage = config.defaultimage; }
   }

}
