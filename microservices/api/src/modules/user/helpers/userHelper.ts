import { User } from '@prisma/client';

import { UserRO } from '../types/userType';

function getUserRO(user: User): UserRO {
	return {
		id: user.id,
		firstName: user.firstName,
		lastName: user.lastName,
		email: user.email,
		role: user.role,
		createdAt: user.createdAt,
		updatedAt: user.updatedAt,
	};
}

export default { getUserRO };
