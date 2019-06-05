import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Lesson, LessonAttempt, Question, Attempt, Course } from '../../models/models';
import { ContentService } from '../../services/content.service';
import { DomSanitizer } from '@angular/platform-browser';
import { config } from 'src/app/config';
import { MatPaginator, MatSort, MatTableDataSource } from '@angular/material';
import { QuestionComponent } from '../question/question.component';
import {MatDialog} from '@angular/material';

export interface QuestionAttempt {
   title: string;
   attempts: number;
   score: number;
   question: Question;
   attempt: Attempt;
}

@Component({
   selector: 'app-lesson',
   templateUrl: './lesson.component.html',
   styleUrls: ['./lesson.component.scss']
})
export class LessonComponent implements OnInit {

   lesson: Lesson;
   course: Course;
   lessonAttempt: LessonAttempt;
   questions: Array<Question> = [];
   attempts: Array<Attempt> = [];
   image: any;
   init = 0;
   // pageindex: number = 0;
   // pagesize: number = 10;
   // searchText: string = '';
   // display: number = 0;
   dataSource: MatTableDataSource<QuestionAttempt>;
   displayedColumns: string[] = ['title', 'attempts', 'score', 'performance'];

   @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
   @ViewChild(MatSort, {static: true}) sort: MatSort;

   constructor(public dialog: MatDialog, private router: Router, private route: ActivatedRoute, private contentService: ContentService,
               private sanitizer: DomSanitizer) {
      const navigation = this.router.getCurrentNavigation();
      if (!navigation || !navigation.extras.state) { return; }
      this.lesson = navigation.extras.state.lesson;
      this.course = navigation.extras.state.course;
      this.image = this.resolveImage(this.lesson.image);
   }

   resolveImage(i: string) {
      if (!i || i == '') { i = config.defaultimage; }
      return this.sanitizer.bypassSecurityTrustStyle(`url(${i})`);
   }

   createNewQA(question: Question, attempt: Attempt): QuestionAttempt {
      return {
         title: question.title,
         attempts: attempt.count,
         score: attempt.score,
         question,
         attempt
      };
   }

   preparedata(): Array<QuestionAttempt> {
      const data = new Array<QuestionAttempt>();
      // tslint:disable-next-line: prefer-const
      for (let question of this.questions) {
         data.push(this.createNewQA(question, this.getquestionattempt(question)));
      }
      console.log(data);
      return data;
   }

   getquestionattempt(q: Question): Attempt {
      let a: Attempt = null;
      if (this.attempts) { a = this.attempts.find(x => x.question === q.id); }
      a = a || new Attempt(q.id);
      return a;
   }

   setup() {
      this.init++;
      if (this.init === 2) {
         console.log('preparing data');
         this.dataSource = new MatTableDataSource<QuestionAttempt>(this.preparedata());
         this.dataSource.paginator = this.paginator;
         this.dataSource.sort = this.sort;
      }
   }

   getperf(row: QuestionAttempt) {
      if (row.attempt.count === 0) { return 0; }
      return row.attempt.totalscore / (row.question.score * row.attempt.count);
   }

   applyFilter(filterValue: string) {
      this.dataSource.filter = filterValue.trim().toLowerCase();

      if (this.dataSource.paginator) {
         this.dataSource.paginator.firstPage();
      }
   }

   openQuestionAttempt(currentQuestion: Question, currentAttempt: Attempt) {
      const dialogRef = this.dialog.open(QuestionComponent, {panelClass: 'full-width-dialog',
         width: '75%',
         // height:"90%"
         data : {
            question : currentQuestion,
            attempt : currentAttempt,
         }
      });
      dialogRef.afterClosed().subscribe(result => {
         // TODO: call tts.stop and stt.stop
         console.log(`Dialog result: ${result}`);
      });
   }

   ngOnInit() {
      if (!this.lesson) {
         this.route.params.subscribe(params => {
            this.contentService.getCourse(params.course).subscribe(data => {
               this.course = data.course;
               this.contentService.getLesson(params.lesson).subscribe(data => {
                  this.lesson = data.lesson;
                  this.lessonAttempt = data.attempt;
                  this.image = this.resolveImage(this.lesson.image);
                  this.contentService.getQuestions(this.course.id, this.lesson.id).subscribe(questions => { this.questions = questions; this.setup(); });
                  this.contentService.getAttempts(this.course.id, this.lesson.id).subscribe(attempts => { this.attempts = attempts; this.setup(); });
               });
            });
         });
      } else {
         this.contentService.getQuestions(this.course.id, this.lesson.id).subscribe(questions => { this.questions = questions; this.setup(); });
         this.contentService.getAttempts(this.course.id, this.lesson.id).subscribe(attempts => { this.attempts = attempts; this.setup(); });
      }
   }

}
