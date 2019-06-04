import { Injectable } from '@angular/core';
import { of, Observable, BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { config } from 'src/app/config';
import { catchError, mapTo, tap } from 'rxjs/operators';
import { Tokens } from '../models/tokens';
import { SocialUser } from 'angularx-social-login';
import { AuthService as SocialAuthService } from 'angularx-social-login';
import { Router } from '@angular/router';

@Injectable({
   providedIn: 'root'
})
export class AuthService {

   private readonly JWT_TOKEN = 'JWT_TOKEN';
   private readonly REFRESH_TOKEN = 'REFRESH_TOKEN';
   private socialUser: BehaviorSubject<SocialUser> = new BehaviorSubject<SocialUser>(null);
   constructor(private http: HttpClient, private socialAuthService: SocialAuthService, private router: Router) {
      // if user is logged in with Google already, it will fireup and login with backend at start
      // this way we need not store our user in localstorage as the social login provider would be doing that.
      this.socialAuthService.authState.subscribe((user) => {
         if (user) {
            console.log('constructor aut state called');
            this.http.post<any>(`${config.apiUrl}/api/token/`, { idtoken: user.idToken, provider: user.provider })
            .subscribe(
               tokens => this.doLoginUser(user, tokens),   // success
               error => console.log(error),                // error
               // ()=>this.router.navigate([this.router.url])           //complete
            );
         }
      });
      // here we ensure that our tokens are valid, else we logout and have user authenticate again
      if (this.isLoggedIn()) {
         console.log('calling refresh token from constructor');
         this.refreshToken();
      }
   }

   // get the current user. We return the behavior subject as observable
   // if no user is loggedin caller will get null
   getLoggedInUser(): Observable<SocialUser> {
      return this.socialUser.asObservable();
   }

   // call sociial signup. We don't manage auth right!
   socialsignin(provider: string): void {
      this.socialAuthService.signIn(provider).catch(reason => console.log(reason));
   }

   logout() {
      this.socialAuthService.signOut().catch(reason => console.log(reason));
      this.socialUser.next(null); // set next user to be null. IMPORTANT
      this.doLogoutUser();
      this.router.navigate(['/']);
   }

   getJwtToken() {
      return localStorage.getItem(this.JWT_TOKEN);
   }

   isLoggedIn() {
      return !!this.getJwtToken();
   }

   // refreshes token, else logs in again, else logs out
   refreshToken(): Observable<boolean> {
      return this.http.post<any>(`${config.apiUrl}/api/token/refresh/`, {
         refreshToken: this.getRefreshToken()
      }).pipe(
         tap((tokens: Tokens) => { this.storeJwtToken(tokens.access); }),
         mapTo(true),
         catchError(e => {
            this.logout();
            return of(false);
         })
      );
   }

   private getRefreshToken() {
      return localStorage.getItem(this.REFRESH_TOKEN);
   }

   private doLogoutUser() {
      this.removeTokens();
   }

   private removeTokens() {
      localStorage.removeItem(this.JWT_TOKEN);
      localStorage.removeItem(this.REFRESH_TOKEN);
   }

   private doLoginUser(user: SocialUser, tokens: Tokens) {
      this.socialUser.next(user);
      this.storeTokens(tokens);
   }

   private storeTokens(tokens: Tokens) {
      localStorage.setItem(this.JWT_TOKEN, tokens.access);
      localStorage.setItem(this.REFRESH_TOKEN, tokens.refresh);
   }

   private storeJwtToken(jwt: string) {
      localStorage.setItem(this.JWT_TOKEN, jwt);
   }

   // PROFILE

   getCollegeList() {
      return this.http.get(`${config.apiUrl}/api/colleges/`);
   }

   getFieldOfStudyList() {
      return this.http.get(`${config.apiUrl}/api/studyfields/`);
   }

   getProfile() {
      return this.http.get(`${config.apiUrl}/interviewprep/profile/`);
   }

   updateProfile(data): Observable<boolean> {
      return this.http.post<any>(`${config.apiUrl}/interviewprep/profile/`, data).pipe(
         mapTo(true),
         catchError(error => {
            return of(false);
         })
      );
   }
}
