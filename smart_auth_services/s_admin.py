from BaseModels import AdminRequest, AdminResponse, AdminUpdate, Details
from database.models import Admin


def addAdmin(admin_request: AdminRequest) -> Details:
    """
    :raise IdentifierExistsError
    :param admin_request:
    :return adminResponse:
    """
    return Admin.addAdmin(admin_request)


def updateAdmin(id_: int, admin_update: AdminUpdate) -> AdminResponse:
    """
    :raise ArgumentError
    :param id_:
    :param admin_update:
    :return AdminResponse:
    """

    return Admin.updateAdmin(id_, admin_update)


def deleteAdmin(id_: int) -> Details:
    """
    :raise ArgumentError
    :param id_:
    :return Details:
    """

    return Admin.deleteAdmin(id_)


def getAdminById(id_: int) -> AdminResponse:
    """
    :param id_:
    :return AdminResponse:
    """
    return Admin.getAdminById(id_)


def getAdminByMail(email: str) -> AdminResponse:
    """
    :param email:
    :return AdminResponse:
    """

    return Admin.getAdminByEmail(email)


def getAllAdmins() -> list[AdminResponse]:
    """
    :return list[AdminResponse]:
    """
    return Admin.getAllAdmins()


if __name__ == '__main__':
    # admin_to_update = AdminUpdate(password_admin='HelloWorld_')
    # print(updateAdmin(3, admin_to_update))
    pass
