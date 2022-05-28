import { AsyncRouter } from 'express-async-router';

import UserController from '../controllers/userController';

import { authenticateAdmin, authenticateOwner } from '../../../middlewares/authenticationHandler';
import meHandler from '../middlewares/meHandler';
import userHandler from '../middlewares/userHandler';
import { UserCreateDTO, UserUpdateDTO } from '../types/userType';
import validate from '../../../middlewares/validationHandler';

const userRouter = AsyncRouter();

userRouter.post('/', validate(UserCreateDTO), UserController.createUser);

userRouter.get('/:userId', meHandler, authenticateOwner, userHandler, UserController.getUser);

userRouter.get('/', authenticateAdmin, UserController.getUsers);

userRouter.patch('/:userId', validate(UserUpdateDTO), meHandler, authenticateOwner, userHandler, UserController.updateUser);

userRouter.delete('/:userId', meHandler, authenticateOwner, userHandler, UserController.deleteUser);

export default userRouter;
