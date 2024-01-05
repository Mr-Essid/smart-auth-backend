import datetime
from typing import Type

from sqlalchemy import (String, Integer, ARRAY, Column, Identity, Boolean, Date, Double, ForeignKey, DateTime, Text,
                        select, func, Row, update)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, relationship, Session

from BaseModels import (AdminRequest, AdminUpdate, Details, AdminResponse, EmployerRequest, EmployerUpdate,
                        EmployerResponse, HistoryResponse, DataOfDayHistory)
from database.mainDB import engine
from utils import sha256

Base = declarative_base()


class ArgumentError(RuntimeError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EmailExistsError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class IdentifierExistsError(RuntimeError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


MAX_USERNAME_LEN = 30
MAX_EMAIL_LEN = 100


class Admin(Base):
    __tablename__ = 'admins'
    id_admin = Column(Integer, Identity(start=1), primary_key=True)
    name_admin = Column(String(30), nullable=False)
    email_admin = Column(String(100), nullable=False, unique=True)
    password_admin = Column(Text, nullable=False)
    is_active = Column(Boolean, default=False)
    create_at = Column(Date)
    authority = Column(Integer, default=1)

    def __init__(self, admin: AdminRequest):
        self.name_admin = admin.name_admin
        self.email_admin = admin.email_admin
        self.password_admin = admin.password_admin
        self.create_at = datetime.date.today()

    @staticmethod
    def validateData(data: AdminRequest):
        if len(data.name_admin) > MAX_USERNAME_LEN:
            raise ArgumentError("Name Too Long")
        if len(data.email_admin) > MAX_EMAIL_LEN:
            raise ArgumentError("Email Too Long")

    @classmethod
    def addAdmin(cls, admin: AdminRequest):
        """
        :param admin:
        :raise IdentifierExistsError
        :return:
        """
        cls.validateData(admin)
        admin.password_admin = sha256(admin.password_admin)
        new_admin = Admin(admin)
        isExistsWithMail = cls._getAdminByEmail(admin.email_admin)
        if isExistsWithMail is not None:
            raise IdentifierExistsError('Identifier found Exception')

        with Session(engine) as session:
            try:
                session.add(new_admin)
                session.commit()
            except IntegrityError as e:
                session.rollback()

        return cls.getAdminByEmail(admin.email_admin)

    @classmethod
    def deleteAdmin(cls, id_: int):
        admin = cls._getAdminById(id_)

        if admin is None:
            raise ArgumentError(f"No Admin With id {id_}")

        with Session(engine) as session:
            session.delete(admin)
            session.commit()

        return Details(message='Admin Deleted')

    @classmethod
    def activeAdmin(cls, id_: int):

        with Session(engine) as session:
            admin = session.query(cls).filter(cls.id_admin == id_).first()

            if admin is None:
                raise ArgumentError(f"No Admin With id {id_}")

            query = update(cls).where(cls.id_admin == id_).values(
                {cls.is_active: True}
            )
            session.execute(query)
            session.commit()

        return Details(message='Admin Activated')

    @classmethod
    def disActiveAdmin(cls, id_: int):

        with Session(engine) as session:
            admin = session.query(cls).filter(cls.id_admin == id_).first()

            if admin is None:
                raise ArgumentError(f"No Admin With id {id_}")

            query = update(cls).where(cls.id_admin == id_).values(
                {cls.is_active: False}
            )
            session.execute(query)
            session.commit()

        return Details(message='Admin Dis-Active')

    @classmethod
    def updateAdmin(cls, id_, adminUpdate: AdminUpdate):
        if adminUpdate.name_admin is None and adminUpdate.password_admin is None:
            raise ArgumentError("You Should Have Filed At Least")
        with Session(engine) as session:
            admin = session.query(cls).filter(cls.id_admin == id_).first()

            if admin is None:
                raise ArgumentError(f'No Admin With id {id_}')

            if adminUpdate.name_admin is not None:
                if 4 <= len(adminUpdate.name_admin) <= 30:
                    admin.name_admin = adminUpdate.name_admin

                else:
                    raise ArgumentError('Invalid Name')

            if adminUpdate.password_admin is not None:
                print(adminUpdate.password_admin)
                admin.password_admin = sha256(adminUpdate.password_admin)

            session.commit()

        return cls.getAdminById(id_)

    @classmethod
    def getAdminById(cls, id_):
        admin = cls._getAdminById(id_)
        if admin:
            return AdminResponse(**admin.__dict__)

    @classmethod
    def _getAdminById(cls, id_: int) -> AdminResponse | None:
        admin_ = None
        with Session(engine) as session:
            admin_ = session.query(cls).filter(cls.id_admin == id_).first()

        if admin_:
            return admin_

    @classmethod
    def getAdminByEmail(cls, email) -> AdminResponse | None:
        admin = cls._getAdminByEmail(email)
        if admin:
            return AdminResponse(**admin.__dict__)

    @classmethod
    def _getAdminByEmail(cls, email):
        admin_ = None
        with Session(engine) as session:
            admin_ = session.query(cls).filter(cls.email_admin == email).first()

        if admin_:
            return admin_

    @classmethod
    def getAllAdmins(cls):
        adminList = None

        with Session(engine) as session:
            admins = session.query(cls).filter(cls.name_admin != 'root').all()

        def parseAdmin(admin: Type[Admin]):
            return AdminResponse(**admin.__dict__)

        list_ = list(map(parseAdmin, admins))

        return list_


class Employer(Base):
    __tablename__ = 'employers'
    id_employer = Column(Integer, Identity(start=1), primary_key=True)
    identifier_employer = Column(String(10), nullable=False, unique=True)
    name_employer = Column(String(30), nullable=False)
    lastname_employer = Column(String(30), nullable=False)
    email_employer = Column(String(100), nullable=False, unique=True)
    create_at = Column(Date, default=datetime.date.today())
    face_coding_employer = Column(ARRAY(Double))
    is_active = Column(Boolean, default=True)
    history = relationship("History", back_populates="employers")

    @classmethod
    def dataValidation(cls, emp: EmployerRequest):
        if len(emp.name_employer) > MAX_USERNAME_LEN or len(emp.lastname_employer) > MAX_USERNAME_LEN or len(
                emp.email_employer) > MAX_EMAIL_LEN:
            raise ArgumentError('Filed Invalid')

        if len(emp.identifier_employer) > 8:
            raise ArgumentError('Identifier Not Valid')

    def __init__(self, employer: EmployerRequest, face_coding: list[float]):
        self.name_employer = employer.name_employer
        self.email_employer = employer.email_employer
        self.identifier_employer = employer.identifier_employer
        self.lastname_employer = employer.lastname_employer
        self.face_coding_employer = face_coding

    @classmethod
    def addEmployer(cls, emp: EmployerRequest, face_coding: list[float]) -> EmployerResponse:
        cls.dataValidation(emp)
        employerExists = cls.getEmployerByMail(emp.email_employer)
        employerExistsIdentifier = cls.getEmployerByIdentifier(emp.identifier_employer)

        if employerExists is not None:
            raise ArgumentError(f'Employer With Mail {emp.email_employer} Exists')

        if employerExistsIdentifier is not None:
            raise IdentifierExistsError(f'Employer With Identifier {emp.identifier_employer} Exists')

        new_employer_ = Employer(emp, face_coding)

        # validation face coding

        # end validation

        with Session(engine) as session:
            try:
                session.add(new_employer_)
                session.commit()
            except IntegrityError as e:
                session.rollback()

        return cls.getEmployerByIdentifier(emp.identifier_employer)

    @classmethod
    def getEmployerById(cls, id_employer) -> EmployerResponse | None:
        employer = cls._getEmployerById(id_employer)

        if employer is None:
            return
        return EmployerResponse(**employer.__dict__)

    @classmethod
    def getEmployerByMail(cls, email):
        employer: Employer | None = None
        with Session(engine) as session:
            employer = session.query(cls).filter(cls.email_employer == email).first()

        if employer is not None:
            return EmployerResponse(**employer.__dict__)

    @classmethod
    def _getEmployerById(cls, id_):
        employer: cls | None = None

        with Session(engine) as session:
            employer = session.query(cls).filter(cls.id_employer == id_).first()

        return employer

    @classmethod
    def updateEmployer(cls, employer_update: EmployerUpdate) -> EmployerResponse:

        with Session(engine) as session:
            employer = session.query(cls).filter(cls.id_employer == employer_update.id_employer).first()

            if employer is None:
                raise ArgumentError(f'There is No Employer With id {employer_update.id_employer}')

            if employer_update.name_employer is not None:
                if 4 <= len(employer_update.name_employer) < 30:
                    employer.name_employer = employer_update.name_employer

                else:
                    raise ArgumentError("Invalid Name Employer name")

            if employer_update.lastname_employer is not None:
                if 4 <= len(employer_update.lastname_employer) < 30:
                    employer.lastname_employer = employer_update.lastname_employer

                else:
                    raise ArgumentError("Invalid Name Employer lastname ")

            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                raise

        return cls.getEmployerById(employer_update.id_employer)

    @classmethod
    def deleteEmployer(cls, id_):
        employer_: None | Employer = None

        with Session(engine) as session:
            employer_ = session.query(cls).filter(cls.id_employer == id_).first()

            if employer_ is None:
                raise ArgumentError(f'No Employer With id {id_}')

            """
                it's just soft delete we can't remove the use cause our application is history based
            """

            employer_.is_active = False
            session.commit()
        return cls.getEmployerById(id_)

    @classmethod
    def getAllEmployers(cls):
        employerList = None

        with Session(engine) as session:
            employerList = session.query(cls).all()

        def parseEmployer(employer_: Type[Employer]):
            return EmployerResponse(**employer_.__dict__)

        new_list = list(map(parseEmployer, employerList))

        return new_list

    @classmethod
    def getEmployerByIdentifier(cls, identifier) -> EmployerResponse | None:
        employer: Employer | None = None

        with Session(engine) as session:
            employer = session.query(cls).filter(cls.identifier_employer == identifier).first()

        if employer:
            return EmployerResponse(**employer.__dict__)

    @classmethod
    def updateFaceCoding(cls, id_, coding: list[float]):

        with Session(engine) as session:
            employer = session.query(cls).filter(cls.id_employer == id_).first()

            if employer is None:
                raise ArgumentError(f'There is No Employer With Id {id_}')

            employer.face_coding_employer = list(coding)

            session.commit()

        return cls.getEmployerById(id_)

    @classmethod
    def searchEmployer(cls, keyword):
        with Session(engine) as session:
            allEmployersByName = session.query(cls).filter(cls.name_employer.like(f"%{keyword}%")).all()
            return allEmployersByName

    @classmethod
    def updateStateEmployer(cls, id_employer, state: Boolean):

        with Session(engine) as session:
            employer = session.query(Employer).filter(id_employer == cls.id_employer).first()

            if employer is None:
                return

            employer.is_active = state
            session.commit()

            return EmployerResponse(**employer.__dict__)

    @classmethod
    def getEmployerWithState(cls, state: bool):
        with Session(engine) as session:
            employers = session.query(cls).filter(cls.is_active == state).all()

        return employers


class History(Base):
    __tablename__ = 'history'
    id_history = Column(Integer, Identity(start=1), primary_key=True)
    id_employer = Column(Integer, ForeignKey('employers.id_employer', onupdate="CASCADE", ondelete="CASCADE"),
                         nullable=False)
    is_active = Column(Boolean, default=True)
    date_employer_enter = Column(DateTime, nullable=False)
    employers = relationship("Employer", back_populates="history")

    def __init__(self, id_employer, datetime_: datetime.datetime):
        self.id_employer = id_employer
        self.date_employer_enter = datetime_

    @classmethod
    def addHistory(cls, emp_id):
        employer: Employer | None = None
        with Session(engine) as session:
            employer = session.query(Employer).filter(Employer.id_employer == emp_id).first()

            if employer is None or not employer.is_active:
                raise ArgumentError(f'There is No Employer With id {emp_id}')

            dateNew = datetime.datetime.now()
            new_history = cls(emp_id, dateNew)
            session.add(new_history)
            session.commit()

        return Details(message='History Added Successfully')

    @classmethod
    def getAllHistory(cls):
        history: None | list[Type[cls]]
        with Session(engine) as session:
            history: list[Type[History]] = session.query(cls).order_by(cls.date_employer_enter.desc()).all()

        def parseHistory(history_: Type[cls]):
            return HistoryResponse(**history_.__dict__)

        parsed_history = list(map(parseHistory, history))

        return parsed_history

    @classmethod
    def getHistoryById(cls, id_):
        history: None | cls

        with Session(engine) as session:
            history = session.query(cls).filter(cls.id_history == id_).first()

        if history is None:
            return None

        if history:
            return HistoryResponse(**history.__dict__)

    @classmethod
    def getHistoryOfEmployer(cls, id_emp):
        historyEmployer: list[Type[cls]] | None = None
        with Session(engine) as session:
            employer = session.query(Employer).filter(Employer.id_employer == id_emp).first()

            if employer is None:
                raise ArgumentError(f'There is No Employer With id {id_emp}')

            historyEmployer = session.query(cls).filter(cls.id_employer == id_emp).all()

            def parseHistory(history: Type[cls]):
                return HistoryResponse(**history.__dict__)

            parsed_history = list(map(parseHistory, historyEmployer))

        return parsed_history

    @classmethod
    def getHistoryAtDate(cls, date: datetime.datetime | datetime.date):

        res: None | list[Type[cls]]
        begin_date = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=0, second=0, minute=0)
        end_date = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=23, second=59, minute=50)

        with Session(engine) as session:
            res = session.query(cls).filter(begin_date < cls.date_employer_enter).filter(
                cls.date_employer_enter < end_date).all()

        def parseHistory(history: Type[cls]):
            return HistoryResponse(**history.__dict__)

        parsed_history = list(map(parseHistory, res))

        return parsed_history

    @classmethod
    def getHistoryByIdentifierEmployer(cls, emp_id: str):

        with Session(engine) as session:
            emp: Employer | None = session.query(Employer).filter(Employer.identifier_employer == emp_id).first()

            if emp is None:
                return None

            def parseHistory(history: Type[History]):
                return HistoryResponse(**history.__dict__)

            list_ = list(map(parseHistory, session.query(cls).filter(cls.id_employer == emp.id_employer).all()))

            return list_

    @classmethod
    def lastFiveDayData(cls):
        dataOfLastFiveDay = None
        with Session(engine) as session:
            dataOfLastFiveDay = session.query(cls.date_employer_enter, func.count(cls.id_employer)).group_by(
                cls.date_employer_enter).order_by(cls.date_employer_enter.desc()).limit(5).all()

        def parseData(data: tuple[datetime.datetime, int]):
            print(data)
            return DataOfDayHistory(day=data[0].date(), howMany=data[1])

        res = list(map(parseData, dataOfLastFiveDay))

        return res


if __name__ == '__main__':
    # new_one = AdminRequest(
    #     name_admin="essid_",
    #     password_admin='password',
    #     email_admin='essid20@go.com'
    # )

    print(History.lastFiveDayData())
    # Admin.addAdmin(new_one)
    # adminToUpdate = AdminUpdate(name_admin='khaled', password_admin='Hello__')
    # print(Admin.getAdminByEmail('root@go.co'))
    # identifier_employer: str
    # name_employer: str
    # lastname_employer: str
    # email_employer: str
    # new_employer = EmployerRequest(identifier_employer='emp03', name_employer='essid', lastname_employer='khaled',
    #                                email_employer='essid03@go.com')
    # print(Employer.addEmployer(new_employer, [3.233, 3.423, -4.423]))
    # print(Employer.deleteEmployer(5))

    # print(History.addHistory(1))

    # print(Employer.getAllEmployers()[0].face_coding_employer)
    # print(Admin.updateAdmin(2, ))
    # print(Employer.getEmployerWithState(False))
