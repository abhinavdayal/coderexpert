export class Course {
    id: number;
    title: string;
    description: string;
    image: string;
    category: string;
    lessoncount: number;
 }

export class CourseAttempt {
    course: number;
    starttime: any;
    lessonAttempts: number;
    lessonsCompleted: number;
    score: number;
 }

export class Lesson {
    id: number;
    title: string;
    description: string;
    image: string;
    questionCount: number;
    attempts: number;
    completed: number;
 }

export class LessonAttempt {
    lesson: number;
    score: number;
    starttime: any;
    lasttime: any;
    questions: number;
    attempts: number;

    constructor(id: number) {
       this.lesson = id;
       this.score = 0;
       this.questions = 0;
       this.attempts = 0;
    }
 }

export class Question {
    id: number;
    title: string;
    question: string;
    speechtext: string;
    visemes: string;
    answer: string;
    score: number;
    attempts: number;
    totalscore: number;
    accuracy: number;
 }

export class Attempt {
    question: number;
    count: number;
    score: number;
    totalscore: number;

    constructor(q) {
        this.question = q;
        this.count = 0;
        this.score = 0;
        this.totalscore = 0;
    }
}

