import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Course, CourseAttempt } from '../../models/models';
import { ContentService } from '../../services/content.service';
import { config } from 'src/app/config';

@Component({
  selector: 'app-course-tile',
  templateUrl: './coursetile.component.html',
  styleUrls: ['./coursetile.component.scss']
})
export class CoursetileComponent implements OnInit {

  constructor(private contentService: ContentService) { }
  @Input() course: Course;
  @Input() subscribed: CourseAttempt = null;
  courseImage: string;

  @Output() didsubscribe = new EventEmitter();

  subscribe() {
     this.contentService.subscribeCourse(this.course.id).subscribe((x) => {
        this.subscribed = x;
        this.didsubscribe.emit({event, attempt: x});
     });
  }



  ngOnInit() {
    this.courseImage = this.course.image;
    if (!this.course.image || this.course.image == '') { this.courseImage = config.defaultimage; }
  }

}
