import { Role } from '@prisma/client';
import { NextFunction, Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';

import { APIException } from '../exceptions/apiException';

function authenticateUser(req: Request, res: Response, next: NextFunction): void {
	if (req.session.user) {
		next();
	} else {
		next(new APIException(StatusCodes.UNAUTHORIZED, 'You must be logged in.'));
	}
}

function isOwner(req: Request, res: Response, next: NextFunction) {
	if (req.params.userId !== req.session.user?.id && req.session.user?.role !== Role.ADMIN) {
		next(new APIException(StatusCodes.FORBIDDEN, "You are not allowed to access other users information's."));
	} else {
		next();
	}
}

function isAdmin(req: Request, res: Response, next: NextFunction) {
	if (req.session.user?.role === Role.ADMIN) {
		next();
	} else {
		next(new APIException(StatusCodes.FORBIDDEN, 'You must be admin to perform this operation'));
	}
}

const authenticateOwner = [authenticateUser, isOwner];
const authenticateAdmin = [authenticateUser, isAdmin];

export { authenticateUser, authenticateOwner, authenticateAdmin };
