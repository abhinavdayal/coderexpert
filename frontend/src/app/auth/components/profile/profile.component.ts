import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl, FormGroupDirective, NgForm } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { MatSnackBar } from '@angular/material';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  profileForm: FormGroup;
  coreProfileForm: FormGroup;
  interviewProfileForm: FormGroup;
  data: any;
  colleges: any;
  studyfields: any;
  years: Array<number> = [];

  constructor(private formBuilder: FormBuilder, private authService: AuthService, private snackBar: MatSnackBar) { }

  createForm() {
    this.coreProfileForm = this.formBuilder.group({
      college: [this.data.profile.college, [Validators.required]],
      fieldofstudy: [this.data.profile.fieldofstudy, [Validators.required]],
      graduation_year: [this.data.profile.graduation_year, [Validators.required]],
      phone: [this.data.profile.phone, [Validators.required]],
    });

    this.interviewProfileForm = this.formBuilder.group({
      english_education: [this.data.interviewprofile.english_education, [Validators.required]],
    });

    this.profileForm = this.formBuilder.group({
      profile: this.coreProfileForm,
      interviewprofile: this.interviewProfileForm,
    });
  }

  ngOnInit() {
    // set years
    const d: number = new Date().getFullYear();
    for (let y = 0; y < 4; y++) {
      this.years.push(y + d);
    }

    this.authService.getFieldOfStudyList().subscribe(l => {
      this.studyfields = l;
    });

    // set colleges
    this.authService.getCollegeList().subscribe(l => {
      this.colleges = l;
    });

    this.authService.getProfile().subscribe(l => {
      this.data = l;
      console.log(this.data);
      this.createForm();
    });


  }

  onSubmit() {
    console.log(this.profileForm.value);
    this.authService.updateProfile(this.profileForm.value).subscribe(status => {
      if (status) {
        this.snackBar.open('profile updated successfully', 'done', {
          duration: 2000,
        });
      } else {
        this.snackBar.open('error updating profile', 'retry', {
          duration: 2000,
        });
      }
    });
  }

}
