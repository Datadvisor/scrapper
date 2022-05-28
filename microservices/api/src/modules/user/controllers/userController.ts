import { Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';

import UserHelper from '../helpers/userHelper';
import UserService from '../services/userService';

import { UserCreateDTO, UserUpdateDTO } from '../types/userType';
import { hashPassword } from '../../../utils/hash';
import { APIException } from '../../../exceptions/apiException';

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

    res.status(StatusCodes.OK).json(updatedUser);
}

async function deleteUser(req: Request, res: Response): Promise<void> {
	await UserService.deleteById(req.user.id);

	res.sendStatus(StatusCodes.NO_CONTENT);
}

export default {
	createUser,
	getUser,
	getUsers,
	updateUser,
	deleteUser,
};
