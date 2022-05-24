import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';

import { API_CONFIG } from './config/config';
import redisClient from './database/redis';
import logger from './utils/logger';

async function main(): Promise<void> {
	const app = express();
	const { host: hostname, port } = API_CONFIG;

	await redisClient.connect();

	app.use(cors());
	app.use(express.json());
	app.use(helmet());
	app.use(morgan('short', { stream: { write: (message) => logger.http(message.trimEnd()) } }));

	app.listen({ hostname, port }, (): void => {
		logger.info(`Server is listening at http://${hostname}:${port}`);
	});
}

void main();
