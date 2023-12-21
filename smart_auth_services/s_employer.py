from BaseModels import EmployerRequest, Details, EmployerUpdate, EmployerResponse
from database.models import Employer


def addEmployer(employer_request: EmployerRequest, face_coding: list[float]) -> Details:
    """
    :raise ArgumentError
    :raise IdentifierExistsError
    :param employer_request:
    :param face_coding:
    :return Details:
    """
    return Employer.addEmployer(employer_request, face_coding)


def updateEmployer(employer_update: EmployerUpdate) -> EmployerResponse:
    """
    :raise ArgumentError
    :param employer_update:
    :return EmployerResponse:
    """

    return Employer.updateEmployer(employer_update)


def deleteEmployer(id_: int) -> Details:
    """
    :raise ArgumentError
    :param id_:
    :return:
    """

    return Employer.deleteEmployer(id_)


def getEmployerByid(id_: int) -> EmployerResponse:
    """
    :param id_:
    :return EmployerResponse | TypeNone:
    """
    return Employer.getEmployerById(id_)


def getEmployerByEmail(email: str) -> EmployerResponse | None:
    """
    :param email:
    :return EmployerResponse | TypeNone:
    """

    return Employer.getEmployerByMail(email)


def getEmployerByIdentifier(identifier: str) -> EmployerResponse | None:
    """
    :param identifier:
    :return EmployerResponse | TypeNone:
    """
    return Employer.getEmployerByIdentifier(identifier)


def getAllEmployers() -> list[EmployerResponse]:
    """
    :return list[EmployerResponse]:
    """
    return Employer.getAllEmployers()


def updateFaceCoding(id_: int, faceCoding: list[float]) -> EmployerResponse:
    """
    :raise Argument Error
    :param id_:
    :param faceCoding:
    :return:
    """
    return Employer.updateFaceCoding(id_, faceCoding)


if __name__ == '__main__':
    print(addEmployer(
        EmployerRequest(name_employer='amine', lastname_employer='essid', identifier_employer='emp04',
                        email_employer='essid001@go.com'), face_coding=[3.323, 42.4323, 0.43243, 2.4234, 0.423]))
