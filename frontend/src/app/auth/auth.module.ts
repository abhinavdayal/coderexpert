import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthGuard } from './guards/auth.guard';
import { AuthService } from './services/auth.service';
import { CourseGuard } from './guards/course.guard';
import { TokenInterceptor } from './token.interceptor';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ProfileComponent } from './components/profile/profile.component';
import { SocialLoginModule, AuthServiceConfig, LoginOpt } from 'angularx-social-login';
import { GoogleLoginProvider } from 'angularx-social-login';
import { AuthComponent } from './components/auth/auth.component';
import { MatIconModule, MatButtonModule, MatCardModule, MatFormFieldModule,
  MatInputModule, MatSelectModule, MatOptionModule, MatAutocompleteModule, MatSnackBarModule, MatDividerModule } from '@angular/material';

const googleLoginOptions: LoginOpt = {
  scope: 'profile email'
}; // https://developers.google.com/api-client-library/javascript/reference/referencedocs#gapiauth2clientconfig

const config = new AuthServiceConfig([
  {
    id: GoogleLoginProvider.PROVIDER_ID,
    provider: new GoogleLoginProvider(
      '3440031025-0ibqq9u77l693gj0ahrf815a86kt5cts.apps.googleusercontent.com',
      googleLoginOptions)
  },
]);

export function provideConfig() {
  return config;
}


@NgModule({
  declarations: [AuthComponent, ProfileComponent],
  providers: [
    AuthGuard, AuthService, CourseGuard,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: TokenInterceptor,
      multi: true
    },
    {
      provide: AuthServiceConfig,
      useFactory: provideConfig
    }
  ],
  imports: [
    CommonModule,
    HttpClientModule,
    RouterModule,
    FormsModule,
    ReactiveFormsModule,
    SocialLoginModule,
    MatIconModule,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatOptionModule,
    MatAutocompleteModule,
    MatSnackBarModule,
    MatDividerModule
  ],
  exports: [AuthComponent]
})
export class AuthModule { }
