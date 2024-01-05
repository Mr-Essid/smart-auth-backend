import base64
import datetime
from typing import Annotated

from starlette import status
from database.models import ArgumentError
from smart_auth_services.s_history import (addHistory, getHistoryById, getAllHistory, getHistoryOfEmployer,
                                           getHistoryOfDate, getHistoryByEmployerIdentifier, getLastFiveDaysHistory)
from fastapi import APIRouter, HTTPException, BackgroundTasks, Header
from dbConfig import MQTT_CLIENT_PASSWORD, MQTT_CLIENT_USERNAME, API_KEY, BROKER_URL
from fastapi_mqtt import MQTTConfig, FastMQTT

config = MQTTConfig(
    username='essid',
    password='HelloWorld_1',
    host='a1bab6f7160c46d9953a7063106f84b9.s1.eu.hivemq.cloud',
    port=8883,
    ssl=True
)

mqttApp = FastMQTT(config)


@mqttApp.on_connect()
def connect(client, p, rc, pr):
    print("Connected")


@mqttApp.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ", topic, payload.decode(), qos, properties)
    return 0


history_router = APIRouter(prefix='/history', tags=['History'])


# set username and password


def syncWithApp():
    mqttApp.publish('/history', 'HelloWorld')
    pass
    # enable TLS for secure connection

    # set username and password


@history_router.post('/{id_}')
def addHistoryC(id_: int, backGroundTask: BackgroundTasks, x_token: Annotated[str | None, Header()] = None):
    print(x_token)
    print(base64.b64encode(API_KEY.encode()))
    if x_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Request Not Authorized"
        )

    if x_token != base64.b64encode(API_KEY.encode()).decode():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Request Not Authorized"
        )

    details = None
    try:
        details = addHistory(id_)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    backGroundTask.add_task(syncWithApp)
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
    mqttApp.publish('/history', 'HelloWorld')
    if history is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"There is No History With id {id_}")

    return history


@history_router.get('/employer/{id_}')
def getHistoryEmployer(id_: int, backGroundTask: BackgroundTasks):
    listHistory = None

    try:
        listHistory = getHistoryOfEmployer(id_)
    except ArgumentError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    return listHistory


@history_router.get('/date')
def getHistoryByDate(date: datetime.date):
    return getHistoryOfDate(date)


@history_router.get('/date/last-five-days')
def getLastFiveDaysC():
    return getLastFiveDaysHistory()
