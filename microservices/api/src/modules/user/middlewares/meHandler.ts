import { NextFunction, Request, Response } from 'express';

function meHandler(req: Request, res: Response, next: NextFunction): void {
	if (req.session.user) {
		req.params.userId = req.params.userId.replace('me', `${req.session.user.id}`);
	}
	next();
}

export default meHandler;
