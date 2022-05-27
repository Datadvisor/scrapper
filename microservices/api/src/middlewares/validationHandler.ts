import { RequestHandler } from 'express';
import handler from 'express-async-handler';
import { validate as classValidator } from 'class-validator';
import type { ClassConstructor } from 'class-transformer';
import { plainToInstance } from 'class-transformer';
import { StatusCodes } from 'http-status-codes';

import { APIException } from '../exceptions/apiException';

function validate<T>(type: ClassConstructor<T>): RequestHandler {
	return handler(async (req, res, next) => {
		const parsedBody = plainToInstance(type, req.body);
		// eslint-disable-next-line @typescript-eslint/ban-types
		const errors = await classValidator(parsedBody as Object, { whitelist: true });

		if (errors.length !== 0) {
			if (!errors[0].constraints) {
				return;
			}

			const message = Object.values(errors[0].constraints)[0];

			next(new APIException(StatusCodes.BAD_REQUEST, message));
		} else {
			req.body = parsedBody;
			next();
		}
	});
}

export default validate;
