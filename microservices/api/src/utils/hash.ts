import bcrypt from 'bcrypt';

import { API_CONFIG } from '../config/config';

async function hashPassword(password: string) {
	return bcrypt.hash(password, API_CONFIG.saltRounds);
}

function verifyPassword(password: string, encryptedPassword: string) {
	return bcrypt.compare(password, encryptedPassword);
}

export { hashPassword, verifyPassword };
