import { StatusCodes } from 'http-status-codes';

export class APIException extends Error {
	public statusCode: StatusCodes;

	constructor(statusCode: StatusCodes, message: string) {
		super(message);
		this.statusCode = statusCode;
	}
}
