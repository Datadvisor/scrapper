import bcrypt from 'bcrypt';
import { v4 as uuidv4 } from 'uuid';

import { API_CONFIG } from '../config/config';

async function hashPassword(password: string) {
	return bcrypt.hash(password, API_CONFIG.saltRounds);
}

function verifyPassword(password: string, encryptedPassword: string) {
	return bcrypt.compare(password, encryptedPassword);
}

function generatePasswordResetToken() {
	return uuidv4();
}

export { hashPassword, verifyPassword, generatePasswordResetToken };
