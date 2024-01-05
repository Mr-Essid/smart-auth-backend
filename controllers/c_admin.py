import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from BaseModels import AdminRequest, Details, AdminUpdate, AdminResponse, Token
from database.models import ArgumentError, IdentifierExistsError
from smart_auth_services.JWTService import create_access_token, decodeAccessToken
from smart_auth_services.s_admin import (addAdmin, updateAdmin, deleteAdmin, getAllAdmins, getAdminById, getAdminByMail,
                                         ActiveAdmin, DisActiveAdmin)
from utils import sha256

admin_route = APIRouter(prefix="/admin", tags=["Admin"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")


def getCurrentAdmin(token=Depends(oauth2_scheme)):
    data = decodeAccessToken(token)
    email = data.get("username")
    return getAdminByMail(email)


@admin_route.post("/signup", response_model=AdminResponse)
def addAdminC(admin: AdminRequest):
    employer = None
    try:
        # all internet sign in admins have to wait until root admin accept there request
        employer = addAdmin(admin)
    except (ArgumentError, IdentifierExistsError) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)

    return employer


@admin_route.get('/current')
def getCurrent(admin: AdminResponse = Depends(getCurrentAdmin)):
    return admin


@admin_route.put("/", response_model=AdminResponse)
def updateAdminC(admin_data: AdminUpdate, current: AdminResponse = Depends(getCurrentAdmin)):
    admin: AdminResponse
    try:
        admin = updateAdmin(current.id_admin, admin_data)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)

    return admin


@admin_route.delete("/", response_model=Details)
def deleteAdminC(currentAdmin: AdminResponse = Depends(getCurrentAdmin)):
    details: Details
    try:
        details = deleteAdmin(currentAdmin.id_admin)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)

    return details


@admin_route.get('/admins', response_model=AdminResponse | list[AdminResponse])
def getAdminsC(email: str | None = None):
    if email is not None:
        admin = getAdminByMail(email)
        if not admin:  # if not None
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Admin With Email {email} Not Found")
        return admin

    return getAllAdmins()


@admin_route.get("/admin/state/update/{id_}/active")
def adminUpdateStatus(id_: int, currentUser: AdminResponse = Depends(getCurrentAdmin)):
    if currentUser.authority != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your Request Is Not Authorized"
        )

    try:
        return ActiveAdmin(id_)
    except ArgumentError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin Not Found"
        )


@admin_route.get("/admin/state/update/{id_}/dis-active")
def adminUpdateStatus(id_: int, currentUser: AdminResponse = Depends(getCurrentAdmin)):
    if currentUser.authority != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your Request Is Not Authorized"
        )

    try:
        return DisActiveAdmin(id_)
    except ArgumentError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin Not Found"
        )


@admin_route.get('/{id_}', response_model=AdminResponse)
def getAdminByIdC(id_: int):
    admin = getAdminById(id_)

    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Admin With id {id_} Not Found")
    return admin


@admin_route.post('/login')
def loginAdmin(formData: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = formData.username
    admin = getAdminByMail(username)

    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if admin.password_admin != sha256(formData.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your Request Is On Process"
        )

    token_ = create_access_token({'username': admin.email_admin})

    all_token = Token(access_token=token_, date_exp=datetime.date.today() + datetime.timedelta(days=1))

    return all_token
