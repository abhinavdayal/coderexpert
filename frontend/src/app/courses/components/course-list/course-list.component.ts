import { Component, OnInit, Input } from '@angular/core';
import { ContentService } from '../../services/content.service';
import { Course, CourseAttempt } from '../../models/models';

@Component({
   selector: 'app-course-list',
   templateUrl: './course-list.component.html',
   styleUrls: ['./course-list.component.scss']
})
export class CourseListComponent implements OnInit {

   @Input() courses: Array<Course> = [];
   @Input() from = 0;
   @Input() to = 10;
   @Input() search = '';
   @Input() category = 'All';
   @Input() onlymycourses = false;

   mycourses: Array<CourseAttempt> = [];
   init = false;


   constructor(private contentService: ContentService) { }

   isSubscribed(id: number) {
      return this.mycourses.length > 0 ? this.mycourses.find(x => x.course == id) : false;
   }

   FilteredCourses(): Array<Course> {
      return this.courses.filter
         (course => {
            return (this.search == '' || course.title.toLowerCase().includes(this.search.toLowerCase()))
               && (this.category == 'All' || course.category == this.category)
               && (!this.onlymycourses || this.isSubscribed(course.id));
         }).sort((a: Course, b: Course) => a.title < b.title ? -1 : 1);
   }

   ngOnInit() {
      this.contentService.getMyCourses().subscribe(mycourses => {
         this.mycourses = mycourses;
         this.init = true;
      });
   }

}
