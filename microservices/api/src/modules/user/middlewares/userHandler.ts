import { NextFunction, Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';

import UserService from '../services/userService';

import { APIException } from '../../../exceptions/apiException';

async function userHandler(req: Request, res: Response, next: NextFunction) {
	const { userId } = req.params;

	try {
		const user = await UserService.findById(userId);

		if (!user) {
			next(new APIException(StatusCodes.NOT_FOUND, 'User not found'));
		} else {
			req.user = user;
			next();
		}
	} catch (err) {
		next(err);
	}
}

export default userHandler;
