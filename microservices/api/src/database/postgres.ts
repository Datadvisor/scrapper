import { PrismaClient } from '@prisma/client';

import { POSTGRES_CONFIG } from '../config/config';
import logger from '../utils/logger';

const postgresClient = new PrismaClient({
	datasources: {
		db: {
			url: `postgresql://${POSTGRES_CONFIG.username}:${POSTGRES_CONFIG.password}@
			${POSTGRES_CONFIG.host}:${POSTGRES_CONFIG.port}/${POSTGRES_CONFIG.database}`,
		},
	},
	log: [
		{
			emit: 'event',
			level: 'error',
		},
		{
			emit: 'event',
			level: 'warn',
		},
		{
			emit: 'event',
			level: 'info',
		},
	],
});

postgresClient.$on('error', (event) => logger.error(event.message));
postgresClient.$on('warn', (event) => logger.warn(event.message));
postgresClient.$on('info', (event) => logger.info(event.message));

export default postgresClient;
