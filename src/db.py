from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Float, PickleType, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from config import params


# Create base class
Base = declarative_base()


class ClientStatus(Base):
    """
    Represents status of a client at a given point in time. These records
    are what makes up the aging report for a given week.
    """

    __tablename__ = 'ClientStatus'

    client_id = Column(Integer, primary_key=True)
    name = Column(String)
    beginning_balance = Column(Float)
    invoices = Column(Float)
    receipts = Column(Float)
    service_charges = Column(Float)
    adjustments = Column(Float)
    zero_to_thirty_days = Column(Float)
    thirty_to_sixty_days = Column(Float)
    sixty_to_ninety_days = Column(Float)
    ninety_to_one_hundred_twenty_days = Column(Float)
    one_hundred_twenty_plus_days = Column(Float)
    ending_balance = Column(Float)
    date_processed = Column(DateTime)

    aging_report_id = Column(Integer, ForeignKey("AgingReport.ar_id"))    # identifies which aging report a given client status belongs to
    aging_report = relationship("AgingReport", back_populates="client_statuses")

    def __init__(self, client_id, name, beginning_balance, invoices, receipts, 
        service_charges, adjustments, day_0_to_30, day_30_to_60, day_60_to_90, 
        day_90_to_120, day_120_plus, ending_balance, date_processed):
        self.client_id = client_id
        self.name = name
        self.beginning_balance = beginning_balance
        self.invoices = invoices
        self.receipts = receipts
        self.service_charges = service_charges
        self.adjustments = adjustments
        self.zero_to_thirty_days = day_0_to_30
        self.thirty_to_sixty_days = day_30_to_60
        self.sixty_to_ninety_days = day_60_to_90
        self.ninety_to_one_hundred_twenty_days = day_90_to_120
        self.one_hundred_twenty_plus_days = day_120_plus
        self.ending_balance = ending_balance
        self.date_processed = Column(DateTime)

    def __repr__(self):
        return f"<ClientStatus(client_id={self.client_id}, name={self.name}, beginning_balance={self.beginning_balance}, invoices={self.invoices}, receipts={self.receipts}, service_charges={self.service_charges}, adjustments={self.adjustments}, day_0_to_30={self.day_0_to_30}, day_30_to_60={self.day_30_to_60}, day_60_to_90={self.day_60_to_90}, day_90_to_120={self.day_90_to_120}, day_120_plus={self.day_120_plus}, ending_balance={self.ending_balance}, date_processed={self.date_processed})>"


class ClientContactInfo(Base):
    """
    Represents the contact info for a given client.
    """

    __tablename__ = "ClientContactInfo"

    client_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

    def __init__(self, client_id, name, email, phone):
        self.client_id = client_id
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f"<ClientContactInfo(client_id={self.client_id}, name={self.name}, email={self.email}, phone={self.phone})>"


class ClientContactHistory(Base):
    """
    Represents a complete history of how and when a client has been contacted
    since the start of service.

    The format of each 'history' type is...

        {contact_datetime: contact_type_identifier_string}

    ...where contact type identifiers refer to different iterations such as 
    'Email A', 'Email B', etc.
    """

    __tablename__ = "ClientContactHistory"

    client_id = Column(Integer, primary_key=True)
    email_history = Column(PickleType)
    text_history = Column(PickleType)
    call_history = Column(PickleType)
    payment_history = Column(PickleType)

    def __init__(self, client_id, email_history, text_history, 
        call_history, payment_history):
        
        self.client_id = client_id
        self.email_history = email_history
        self.text_history = text_history
        self.call_history = call_history
        self.payment_history = payment_history

    def __repr__(self):
        return f"<ClientContactHistory(client_id={self.client_id}, email_history={self.email_history}, text_history={self.text_history}, call_history={self.call_history}, payment_history={self.payment_history})>"


class AgingReport(Base):
    """
    Tracks the name of all aging reports that have already been processed for a 
    given project.
    """

    __tablename__ = "AgingReport"

    ar_id = Column(Integer, primary_key=True)
    filename = Column(String)
    date_processed = Column(DateTime)

    client_statuses = relationship("ClientStatus", order_by=ClientStatus.client_id, back_populates="aging_report")
    
    def __init__(self, ar_id, filename, date_processed):
        self.ar_id = ar_id
        self.filename = filename
        self.date_processed = date_processed

    def __repr__(self):
        return f"<AgingReportHistory(report_number={self.ar_id}, filename={self.filename}, date_processed={self.date_processed})>"


def db_init():

    # Connect with database via engine
    engine = create_engine(params['database_url'], echo=True, future=True)

    # Create database from all classes
    Base.metadata.create_all(engine)

    return engine

