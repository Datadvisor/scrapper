import expressSession from 'express-session';
import connectRedis from 'connect-redis';

import { API_CONFIG } from '../config/config';
import redisClient from '../database/redis';

const RedisStore = connectRedis(expressSession);

const session = expressSession({
	secret: API_CONFIG.sessionSecret,
	cookie: { httpOnly: false, secure: 'auto' },
	resave: false,
	saveUninitialized: false,
	store: new RedisStore({ client: redisClient }),
});

export default session;
