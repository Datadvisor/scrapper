import { Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';

import UserHelper from '../helpers/userHelper';
import UserService from '../services/userService';

async function getUser(req: Request, res: Response): Promise<void> {
	res.status(StatusCodes.OK).json(UserHelper.getUserRO(req.user));
}

async function getUsers(req: Request, res: Response): Promise<void> {
	const users = await UserService.findAll();

	res.status(StatusCodes.OK).json(users.map(UserHelper.getUserRO));
}

async function deleteUser(req: Request, res: Response): Promise<void> {
	await UserService.deleteById(req.user.id);

	res.sendStatus(StatusCodes.NO_CONTENT);
}

export default {
	getUser,
	getUsers,
	deleteUser,
};
