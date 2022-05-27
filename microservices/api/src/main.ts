import express from 'express';
import cors from 'cors';
import helmet from 'helmet';

import { API_CONFIG } from './config/config';
import redisClient from './database/redis';
import errorHandler from './middlewares/errorHandler';
import requestLogger from './middlewares/requestLogger';
import session from './middlewares/sessionHandler';
import authRouter from './modules/auth/routes/authRoute';
import userRouter from './modules/user/routes/userRoute';
import logger from './utils/logger';

async function main(): Promise<void> {
	const app = express();
	const { host: hostname, port } = API_CONFIG;

	await redisClient.connect();

	app.use(cors({ origin: API_CONFIG.origin.split(','), credentials: true }));
	app.use(express.json());
	app.use(helmet());
	app.use(requestLogger);
	app.use(session);

	app.enable('trust proxy');

	app.use('/auth', authRouter);
	app.use('/users', userRouter);

	app.use(errorHandler);

	app.listen({ hostname, port }, (): void => {
		logger.info(`Server is listening at http://${hostname}:${port}`);
	});
}

void main();
