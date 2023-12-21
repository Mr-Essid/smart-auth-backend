import datetime

from starlette import status

from database.models import ArgumentError
from smart_auth_services.s_history import (addHistory, getHistoryById, getAllHistory, getHistoryOfEmployer,
                                           getHistoryOfDate, getHistoryByEmployerIdentifier)
from fastapi import APIRouter, HTTPException

history_router = APIRouter(prefix='/history', tags=['History'])


@history_router.post('/{id_}')
def addHistoryC(id_: int):
    details = None
    try:
        details = addHistory(id_)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    return details


@history_router.get('/')
def getAllHistoryC():
    return getAllHistory()


@history_router.get('/identifier/{id_}')
def getHistoryByIdC(id_: str):
    history = getHistoryByEmployerIdentifier(id_)
    if history is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No History With Identifier {id_}")

    return history


@history_router.get("/id/{id_}")
def getHistory(id_: int):
    history = getHistoryById(id_)

    if history is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"There is No History With id {id_}")

    return history


@history_router.get('/employer/{id_}')
def getHistoryEmployer(id_: int):
    listHistory = None

    try:
        listHistory = getHistoryOfEmployer(id_)

    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return listHistory


@history_router.get('/date')
def getHistoryByDate(date: datetime.date):
    return getHistoryOfDate(date)
