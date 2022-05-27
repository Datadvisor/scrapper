import morgan from 'morgan';

import logger from '../utils/logger';

const requestLogger = morgan('short', {
	stream: {
		write(message: string) {
			logger.http(message.trimEnd());
		},
	},
});

export default requestLogger;
