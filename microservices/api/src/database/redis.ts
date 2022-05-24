import * as redis from 'redis';

import { REDIS_CONFIG } from '../config/config';
import logger from '../utils/logger';

const redisClient = redis.createClient({
	socket: {
		host: REDIS_CONFIG.host,
		port: REDIS_CONFIG.port,
	},
	password: REDIS_CONFIG.password,
});

redisClient.on('error', (event) => logger.error(event));
redisClient.on('warn', (event) => logger.warn(event));
redisClient.on('info', (event) => logger.info(event));

export default redisClient;
