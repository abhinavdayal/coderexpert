import { SocialUser } from 'angularx-social-login';

export class User {
    socialprofile: SocialUser;
    hasProfile: boolean;

    constructor(socialuser: SocialUser) {
        this.socialprofile = socialuser;
        this.hasProfile = false;
    }
}
