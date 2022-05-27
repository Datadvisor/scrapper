import { AsyncRouter } from 'express-async-router';

import AuthController from '../controllers/authController';

import validate from '../../../middlewares/validationHandler';
import { AuthSigninDTO } from '../types/authType';
import { authenticateUser } from '../../../middlewares/authenticationHandler';

const authRouter = AsyncRouter();

authRouter.post('/signin', validate(AuthSigninDTO), AuthController.signin);

authRouter.post('/signout', authenticateUser, AuthController.signout);

authRouter.get('/google', AuthController.signinWithGoogle);

export default authRouter;
