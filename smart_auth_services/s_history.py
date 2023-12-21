import datetime

from database.models import History


def addHistory(id_: int):
    """
    :raise ArgumentError
    :param id_:
    :return:
    """
    return History.addHistory(id_)


def getAllHistory():
    return History.getAllHistory()


def getHistoryOfEmployer(id_: int):
    return History.getHistoryOfEmployer(id_)


def getHistoryById(id_: int):
    return History.getHistoryById(id_)


def getHistoryByEmployerIdentifier(identifier: str):
    return History.getHistoryByIdentifierEmployer(identifier)


def getHistoryOfDate(date: datetime.date | datetime.datetime):
    return History.getHistoryAtDate(date)
