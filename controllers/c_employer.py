import cv2
import face_recognition
import numpy as np
from starlette import status

from BaseModels import EmployerRequest, EmployerResponse, AdminResponse, Details, EmployerUpdate
from database.models import ArgumentError, IdentifierExistsError
from smart_auth_services.s_employer import (addEmployer, updateEmployer, deleteEmployer, getEmployerByid,
                                            getEmployerByEmail, getAllEmployers, getEmployerByIdentifier,
                                            updateFaceCoding)
from fastapi import APIRouter, UploadFile, HTTPException, Form

employer_router = APIRouter(prefix="/employer", tags=["Employer"])


@employer_router.post("/")
async def addEmployerC(file: UploadFile, name=Form(max_length=30, min_length=4),
                       lastname=Form(min_length=4, max_length=30), email=Form(min_length=4, max_length=100),
                       identifier=Form(max_length=30)):
    content_file = await file.read()
    np_array = np.frombuffer(content_file, dtype=np.uint8)
    mat = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    codings = face_recognition.face_encodings(mat)

    if len(codings) != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad image Error in conding")

    employer = EmployerRequest(
        name_employer=name,
        lastname_employer=lastname,
        email_employer=email,
        identifier_employer=identifier
    )
    details: Details
    try:
        details = addEmployer(employer, codings[0])
    except (ArgumentError, IdentifierExistsError) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)

    return details


@employer_router.put("/")
def updateEmployerC(dataEmployerToUpdate: EmployerUpdate):
    employer: EmployerResponse

    try:
        employer = updateEmployer(dataEmployerToUpdate)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return employer


@employer_router.put('/face-coding/{id_}', response_model=EmployerResponse)
async def updateFaceCodingC(file: UploadFile, id_: int):
    content_file = await file.read()
    np_array = np.frombuffer(content_file, dtype=np.uint8)
    mat = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    codings = face_recognition.face_encodings(mat)
    if len(codings) != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad image Error in conding")

    employer: EmployerResponse

    try:
        employer = updateFaceCoding(id_, codings[0])

    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return employer


@employer_router.delete('/{id_}')
def deleteEmployerC(id_: int):
    detail: Details
    try:
        detail = deleteEmployer(id_)

    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return detail


@employer_router.get('/')
def getEmployersC(email: str | None = None):
    if email:
        employer = getEmployerByEmail(email)
        if employer is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"There is No Employer With Mail {email}")

        return employer

    return getAllEmployers()


@employer_router.get('/{id_}')
def getEmployerById(id_: int):
    employer = getEmployerByid(id_)
    if employer is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'There Is No Employer With id {id_}')

    return employer


@employer_router.get('/identifier/{ident}')
def getEmployerByIdentifierC(ident_: str):
    employer = getEmployerByIdentifier(ident_)
    if employer is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"There is No Employer With Identifier {ident_}")

    return employer
