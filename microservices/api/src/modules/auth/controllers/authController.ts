import { Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';

import UserHelper from '../../user/helpers/userHelper';
import UserService from '../../user/services/userService';

import { APIException } from '../../../exceptions/apiException';
import { AuthSigninDTO } from '../types/authType';
import { verifyPassword } from '../../../utils/hash';

async function signin(req: Request, res: Response): Promise<void> {
	const payload: AuthSigninDTO = req.body;
	const user = await UserService.findByEmail(payload.email);

	if (!user || !user.password || !(await verifyPassword(payload.password, user.password))) {
		throw new APIException(StatusCodes.UNAUTHORIZED, 'Invalid email and password.');
	}

	req.session.user = {
		id: user.id,
		role: user.role,
	};
	res.status(StatusCodes.OK).json(UserHelper.getUserRO(user));
}

async function signout(req: Request, res: Response): Promise<void> {
	await new Promise<void>((resolve, reject) => {
		req.session.destroy((err) => {
			if (err) {
				reject(err);
			} else {
				resolve();
			}
		});
	});
	res.sendStatus(StatusCodes.NO_CONTENT);
}

// eslint-disable-next-line @typescript-eslint/no-empty-function
async function signinWithGoogle(): Promise<void> {}

export default {
	signin,
	signout,
	signinWithGoogle,
};
