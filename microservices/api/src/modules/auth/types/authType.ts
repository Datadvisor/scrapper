import { IsEmail, IsString } from 'class-validator';

export class AuthSigninDTO {
	@IsEmail({}, { message: "This email is invalid. Make sure it's written like example@email.com." })
	email!: string;

	@IsString({ message: 'You need to enter a password.' })
	password!: string;
}
