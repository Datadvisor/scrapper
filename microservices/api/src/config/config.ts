import * as envVar from 'env-var';
import * as dotenv from 'dotenv';

dotenv.config();

const env = (key: string, required = true) => envVar.get(key).required(required);

export const API_CONFIG = {
	host: env('API_HOST').asString(),
	port: env('API_PORT').asString(),
	origin: env('API_ORIGIN').asString(),
	saltRounds: env('API_SALT_ROUNDS').asInt(),
	sessionSecret: env('API_SESSION_SECRET').asString(),
	logAccessPath: env('API_ACCESS_LOG_PATH').asString(),
	logCombinedPath: env('API_COMBINED_LOG_PATH').asString(),
	logErrorPath: env('API_ERROR_LOG_PATH').asString(),
	sendGridApiKey: env('SEND_GRID_API_KEY').asString(),
};

export const POSTGRES_CONFIG = {
	host: env('POSTGRES_HOST').asString(),
	port: env('POSTGRES_PORT').asPortNumber(),
	username: env('POSTGRES_USER').asString(),
	password: env('POSTGRES_PASSWORD').asString(),
	database: env('POSTGRES_DATABASE').asString(),
};

export const REDIS_CONFIG = {
	host: env('REDIS_HOST').asString(),
	port: env('REDIS_PORT').asPortNumber(),
	password: env('REDIS_PASSWORD').asString(),
};
