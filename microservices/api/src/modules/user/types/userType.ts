import { Role, User } from '@prisma/client';

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

export interface UserRO extends RO {
	id: string;
	firstName: string;
	lastName: string;
	email: string;
	role: Role;
	createdAt: Date;
	updatedAt: Date;
}
