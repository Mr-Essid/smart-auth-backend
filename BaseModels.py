import datetime

from pydantic import BaseModel

"""
    TODO ADMIN BASE MODELS
"""


class AdminRequest(BaseModel):
    name_admin: str
    email_admin: str
    password_admin: str
    is_active: bool = True


class Details(BaseModel):
    message: str


class AdminResponse(AdminRequest):
    id_admin: int
    create_at: datetime.date | None


class AdminUpdate(BaseModel):
    """
    :param name_admin optional\n
    :param password_admin optional
    """

    name_admin: str | None = None
    password_admin: str | None = None


"""
    TODO EMPLOYER BASEMODEL
"""


class EmployerRequest(BaseModel):
    """
    :param identifier_employer\n
    :param name_employer\n
    :param lastname_employer\n
    :param email_employer
    """

    identifier_employer: str
    name_employer: str
    lastname_employer: str
    email_employer: str


class EmployerResponse(EmployerRequest):
    id_employer: int
    create_at: datetime.date
    face_coding_employer: list[float]


class EmployerUpdate(BaseModel):
    """
    :param id_employer \n
    :param name_employer optional\n
    :param lastname_employer optional
    """

    id_employer: int
    name_employer: str | None = None
    lastname_employer: str | None = None


"""
TODO HISTORY BASEMODEL
"""


class HistoryResponse(BaseModel):
    id_history: int
    id_employer: int
    date_employer_enter: datetime.datetime
    is_active: bool


"""
TODO TOKEN
"""


class Token(BaseModel):
    access_token: str
    date_exp: datetime.date
