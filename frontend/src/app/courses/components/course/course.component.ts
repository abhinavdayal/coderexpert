import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Course, Lesson, LessonAttempt} from '../../models/models';
import { ContentService } from '../../services/content.service';
import { DomSanitizer } from '@angular/platform-browser';
import { config } from 'src/app/config';

@Component({
   selector: 'app-course',
   templateUrl: './course.component.html',
   styleUrls: ['./course.component.scss']
})
export class CourseComponent implements OnInit {

   course: Course;
   category: string;
   subscribed: boolean;
   image: any;
   lessons: Array<Lesson> = [];
   lessonattempts: Array<LessonAttempt> = [];
   // MatPaginator Output
   pageindex = 0;
   pagesize = 10;
   searchText = '';
   display = 0;
   init = 0;

   constructor(private router: Router, private contentService: ContentService,
               private sanitizer: DomSanitizer, private route: ActivatedRoute) {
      const navigation = this.router.getCurrentNavigation();
      if (!navigation || !navigation.extras.state) { return; }
      this.course = navigation.extras.state.course;
      this.category = navigation.extras.state.category;
      this.subscribed = navigation.extras.state.subscribed;
      this.image = this.resolveImage(this.course.image);
   }

   resolveImage(i: string) {
      if (!i || i === '') { i = config.defaultimage; }
      return this.sanitizer.bypassSecurityTrustStyle(`url(${i})`); ;
   }

   ngOnInit() {
      this.init = 0;
      if (!this.course) {
         this.route.params.subscribe(params => {
            console.log(params.course);
            this.contentService.getCourse(params.course).subscribe(data => {
               this.course = data['course'];
               this.subscribed = data['attempt'];
               this.image = this.resolveImage(this.course.image);
               this.contentService.getLessons(this.course.id).subscribe(lessons => { this.lessons = lessons; this.init++; });
               this.contentService.getLessonAttempts(this.course.id).subscribe(attempts => { this.lessonattempts = attempts; this.init++; });
            });
         });
      } else {
         this.contentService.getLessons(this.course.id).subscribe(lessons => { this.lessons = lessons; this.init++; });
         this.contentService.getLessonAttempts(this.course.id).subscribe(attempts => { this.lessonattempts = attempts; this.init++; });
      }
   }

}
