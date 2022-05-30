import { Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';
import sgMail from '@sendgrid/mail';

import UserHelper from '../helpers/userHelper';
import UserService from '../services/userService';
import { API_CONFIG } from '../../../config/config';

import { UserCreateDTO, UserUpdateDTO } from '../types/userType';
import { hashPassword, generatePasswordResetToken } from '../../../utils/hash';
import { APIException } from '../../../exceptions/apiException';

sgMail.setApiKey(API_CONFIG.sendGridApiKey);

async function createUser(req: Request, res: Response): Promise<void> {
	const payload: UserCreateDTO = req.body;
	const userExists = await UserService.findByEmail(payload.email);

	if (userExists) {
		throw new APIException(StatusCodes.CONFLICT, 'A user with this email already exists.');
	}

	payload.password = await hashPassword(payload.password);
	const newUser = await UserService.create(payload);

	res.status(StatusCodes.CREATED).json(UserHelper.getUserRO(newUser));
}

async function getUser(req: Request, res: Response): Promise<void> {
	res.status(StatusCodes.OK).json(UserHelper.getUserRO(req.user));
}

async function getUsers(req: Request, res: Response): Promise<void> {
	const users = await UserService.findAll();

	res.status(StatusCodes.OK).json(users.map(UserHelper.getUserRO));
}

async function updateUser(req: Request, res: Response): Promise<void> {
    const payload: UserUpdateDTO = req.body;

	if (payload.password) {
		payload.password = await hashPassword(payload.password);
	}

	const updatedUser = await UserService.updateById(req.user.id, payload);

	res.sendStatus(StatusCodes.OK).json(updatedUser);
}

async function deleteUser(req: Request, res: Response): Promise<void> {
	await UserService.deleteById(req.user.id);

	res.sendStatus(StatusCodes.NO_CONTENT);
}

async function askResetUserPassword(req: Request, res: Response): Promise<void> {
	const payload: UserUpdateDTO = req.body;

	if (!payload.email) {
		throw new APIException(StatusCodes.BAD_REQUEST, 'Email concerned by the password reset is required.');
	}
	const retrievedUser = await UserService.findByEmail(payload.email);
	if (!retrievedUser) {
		throw new APIException(StatusCodes.NOT_FOUND, 'No user found with this email.');
	}
	const userId = retrievedUser.id;
	const generatedPasswordResetToken = generatePasswordResetToken();
	await UserService.updateById(userId, {
		resetPasswordToken: generatedPasswordResetToken,
	});
	const msg = {
		to: payload.email,
		from: 'contact@datadvisor.me',
		subject: 'Datadvisor - Reset your password',
		text: `Hi ${retrievedUser.firstName}, please click on the following link to reset your password: ${API_CONFIG.origin}/users/reset-password/verify/${generatedPasswordResetToken}`,
		html: `Hi ${retrievedUser.firstName}, please click on the following link to reset your password: ${API_CONFIG.origin}/users/reset-password/verify/${generatedPasswordResetToken}`,
	};
	sgMail.send(msg).then(
		() => {},
		(error) => {
			console.error(error);

			if (error.response) {
				console.error(error.response.body);
			}
		},
	);
	res.status(StatusCodes.OK);
}

async function checkResetUserPassword(req: Request, res: Response): Promise<void> {
	const resetToken = req.params.token;

	const retrievedUser = await UserService.findByResetToken(resetToken);
	if (!retrievedUser) {
		throw new APIException(StatusCodes.UNAUTHORIZED, 'The password reset token is invalid or expired.');
	}
	res.status(StatusCodes.OK).json(retrievedUser);
}

async function resetUserPassword(req: Request, res: Response): Promise<void> {
	const payload: UserUpdateDTO = req.body;
	const resetToken = req.params.token;

	if (!payload.password) {
		throw new APIException(StatusCodes.BAD_REQUEST, 'Your new password is required.');
	}
	const retrievedUser = await UserService.findByResetToken(resetToken);
	if (!retrievedUser) {
		throw new APIException(StatusCodes.UNAUTHORIZED, 'The password reset token is invalid or expired.');
	}
	const userId = retrievedUser.id;
	await UserService.updateById(userId, {
		password: await hashPassword(payload.password),
		resetPasswordToken: '',
	});
	res.status(StatusCodes.OK);
}

export default {
	createUser,
	getUser,
	getUsers,
	updateUser,
	deleteUser,
	askResetUserPassword,
	checkResetUserPassword,
	resetUserPassword,
};
