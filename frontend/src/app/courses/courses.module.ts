import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CoursesRoutingModule } from './courses-routing.module';
import { CourseComponent } from './components/course/course.component';
import { CourseListComponent } from './components/course-list/course-list.component';
import { CourseTileComponent } from './components/course-tile/course-tile.component';
import { HomeComponent } from './components/home/home.component';
import { LessonComponent } from './components/lesson/lesson.component';
import { LessonListComponent } from './components/lesson-list/lesson-list.component';
import { LessonTileComponent } from './components/lesson-tile/lesson-tile.component';
import { QuestionComponent } from './components/question/question.component';
import { QuestionListComponent } from './components/question-list/question-list.component';
import { FormsModule } from '@angular/forms';
import { MatIconModule, MatCardModule, MatButtonModule, MatListModule, MatPaginatorModule,
         MatFormFieldModule, MatInputModule, MatSelectModule, MatCheckboxModule, MatTableModule,
         MatSortModule, MatProgressBarModule, MatDialogModule } from '@angular/material';

@NgModule({
  declarations: [
    CourseComponent,
    CourseListComponent,
    CourseTileComponent,
    HomeComponent,
    LessonComponent,
    LessonListComponent,
    LessonTileComponent,
    QuestionComponent,
    QuestionListComponent
  ],
  imports: [
    CommonModule,
    CoursesRoutingModule,
    MatIconModule, MatCardModule, MatButtonModule, MatListModule, MatPaginatorModule,
    MatFormFieldModule, MatInputModule, MatSelectModule, FormsModule,
    MatCheckboxModule, MatTableModule, MatSortModule, MatProgressBarModule, MatDialogModule
  ]
})
export class CoursesModule { }
