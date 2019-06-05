import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { CourseComponent } from './components/course/course.component';
import { LessonComponent } from './components/lesson/lesson.component';

const routes: Routes = [
   {
      path: '',
      component: HomeComponent
   },
   {
      path: ':course',
      component: CourseComponent
   },
   {
      path: ':course/:lesson',
      component: LessonComponent
   }
];

@NgModule({
   imports: [RouterModule.forChild(routes)],
   exports: [RouterModule]
})
export class CoursesRoutingModule { }
