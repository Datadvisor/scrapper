import { AsyncRouter } from 'express-async-router';

import UserController from '../controllers/userController';

import { authenticateAdmin, authenticateOwner } from '../../../middlewares/authenticationHandler';
import meHandler from '../middlewares/meHandler';
import userHandler from '../middlewares/userHandler';

const userRouter = AsyncRouter();

userRouter.get('/:userId', meHandler, authenticateOwner, userHandler, UserController.getUser);

userRouter.get('/', authenticateAdmin, UserController.getUsers);

userRouter.delete('/:userId', meHandler, authenticateOwner, userHandler, UserController.deleteUser);

export default userRouter;
