import { Component, OnInit } from '@angular/core';
import { ContentService } from '../../services/content.service';
import { Course } from '../../models/models';

@Component({
   selector: 'app-home',
   templateUrl: './home.component.html',
   styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
   courses: Array<Course> = [];
   // MatPaginator Output
   pageindex = 0;
   pagesize = 10;
   searchText = '';
   selectedCategory = 0;
   onlymycourses = false;

   constructor(private contentService: ContentService) {

   }

   ngOnInit() {
      this.contentService.getCourses().subscribe(courses => { this.courses = courses; });
   }

}
