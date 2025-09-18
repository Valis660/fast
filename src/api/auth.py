from fastapi import APIRouter, HTTPException, Response
from fastapi_cache.decorator import cache
from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectAlreadyExistsException, UserEmailAlreadyExistsHTTPException, \
    UserAlreadyExistsException, EmailNotRegisteredException, EmailNotRegisteredHTTPException, \
    IncorrectPasswordException, IncorrectPasswordHTTPException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException

    # Автоматически входим в систему после регистрации
    access_token = await AuthService(db).login_user(data)
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
@cache(expire=10)
async def get_me(db: DBDep, user_id: UserIdDep):
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def logout(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}
