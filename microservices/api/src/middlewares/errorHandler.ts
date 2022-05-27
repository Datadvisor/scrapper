import { NextFunction, Request, Response } from 'express';
import { getReasonPhrase, StatusCodes } from 'http-status-codes';

import { RO } from '../types/responseObject';

import logger from '../utils/logger';

// eslint-disable-next-line @typescript-eslint/no-explicit-any,@typescript-eslint/no-unused-vars
function errorHandler(err: any, req: Request, res: Response, _: NextFunction): void {
	const ro: RO = {};
	let statusCode: StatusCodes;

	if (err.statusCode) {
		statusCode = err.statusCode;
		ro.error = {
			statusCode,
			message: err.message,
		};
	} else {
		statusCode = StatusCodes.INTERNAL_SERVER_ERROR;
		ro.error = {
			statusCode,
			message: getReasonPhrase(statusCode),
		};

		logger.error(err);
	}

	res.status(statusCode).json(ro);
}

export default errorHandler;
