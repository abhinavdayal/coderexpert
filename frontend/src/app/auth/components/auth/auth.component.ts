import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { SocialUser } from 'angularx-social-login';
import { GoogleLoginProvider } from 'angularx-social-login';
import { Router } from '@angular/router';
@Component({
   selector: 'app-auth',
   templateUrl: './auth.component.html',
   styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {

   user: SocialUser;

   constructor(private authService: AuthService, private router: Router) { }

   ngOnInit() {
      this.authService.getLoggedInUser().subscribe(user => this.user = user);
   }

   signInWithGoogle(): void {
      this.authService.socialsignin(GoogleLoginProvider.PROVIDER_ID);
   }

   signOut(): void {
      this.authService.logout();
   }

}
