import { User } from '@prisma/client';

import postgresClient from '../../../database/postgres';
import { UserCreateDTO } from '../types/userType';

async function create(payload: UserCreateDTO): Promise<User> {
	return postgresClient.user.create({
		data: payload,
	});
}

async function findById(id: string): Promise<User | null> {
	return postgresClient.user.findUnique({
		where: { id },
	});
}

async function findByEmail(email: string): Promise<User | null> {
	return postgresClient.user.findUnique({
		where: { email },
	});
}

async function findAll(): Promise<User[]> {
	return postgresClient.user.findMany({
		orderBy: { createdAt: 'desc' },
	});
}

async function deleteById(id: string): Promise<User> {
	return postgresClient.user.delete({
		where: { id },
	});
}

export default {
	create,
	findById,
	findByEmail,
	findAll,
	deleteById,
};
