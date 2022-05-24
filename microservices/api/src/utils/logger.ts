import winston from 'winston';

import { API_CONFIG } from '../config/config';

enum LogSeverity {
	ERROR = 'error',
	INFO = 'info',
	HTTP = 'http',
	DEBUG = 'debug',
}

const levels = {
	error: 0,
	warn: 1,
	info: 2,
	http: 3,
	debug: 4,
};

const logFormat = winston.format.printf((info) => `${info.timestamp} [${info.level}]: ${info.message}`);

const filterAccess = winston.format((info) => {
	if (info.level === LogSeverity.HTTP) return info;
	return false;
});

const logger = winston.createLogger({
	levels: levels,
	transports: [
		new winston.transports.Console({
			level: LogSeverity.DEBUG,
			format: winston.format.combine(winston.format.timestamp(), winston.format.colorize(), logFormat),
		}),
		new winston.transports.File({
			level: LogSeverity.HTTP,
			filename: `${API_CONFIG.logAccessPath}`,
			format: winston.format.combine(
				filterAccess(),
				winston.format.timestamp(),
				winston.format.colorize(),
				logFormat,
			),
		}),
		new winston.transports.File({
			level: LogSeverity.INFO,
			filename: `${API_CONFIG.logCombinedPath}`,
			format: winston.format.combine(winston.format.timestamp(), winston.format.colorize(), logFormat),
		}),
		new winston.transports.File({
			level: LogSeverity.ERROR,
			filename: `${API_CONFIG.logErrorPath}`,
			format: winston.format.combine(winston.format.timestamp(), winston.format.colorize(), logFormat),
		}),
	],
});

export default logger;
