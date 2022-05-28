import { Role, User } from '@prisma/client';
import { IsEmail, IsOptional, IsString, MaxLength, MinLength } from 'class-validator';

import { RO } from '../../../types/responseObject';

interface UserSession {
	id: string;
	role: Role;
}

declare global {
	// eslint-disable-next-line @typescript-eslint/no-namespace
	namespace Express {
		interface Request {
			user: User;
		}
	}
}

declare module 'express-session' {
	interface SessionData {
		user: UserSession;
	}
}

export class UserCreateDTO {
	@IsEmail({ message: "This email is invalid. Make sure it's written like example@email.com." })
	email!: string;

	@IsString({ message: 'You need to enter your first name.' })
	firstName!: string;

	@IsString({ message: 'You need to enter your last name.' })
	lastName!: string;

	@IsString({ message: 'You need to enter a password.' })
	@MinLength(8, { message: 'Your password is too short.' })
	@MaxLength(64, { message: 'Your password is too long.' })
	password!: string;
}

export class UserUpdateDTO {
    @IsEmail({ message: "This email is invalid. Make sure it's written like example@email.com." })
    @IsOptional()
    email?: string;

    @IsString()
    @MinLength(8, { message: 'Your password is too short.' })
    @MaxLength(64, { message: 'Your password is too long.' })
    @IsOptional()
    password?: string;
}

export interface UserRO extends RO {
	id: string;
	firstName: string;
	lastName: string;
	email: string;
	role: Role;
	createdAt: Date;
	updatedAt: Date;
}
