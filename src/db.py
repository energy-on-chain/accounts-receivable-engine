from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, PickleType
from sqlalchemy.ext.declarative import declarative_base


# Create base class
Base = declarative_base()


class AgingReport(Base):
    """
    Represents the aging report for a given week. Contains records of which 
    clients have outstanding balances.
    """

    __tablename__ = 'AgingReport'

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

    def __init__(self, client_id, name, beginning_balance, invoices, receipts, service_charges, adjustments, zero_to_thirty_days, thirty_to_sixty_days, sixty_to_ninety_days, ninety_to_one_hundred_twenty_days, one_hundred_twenty_plus_days, ending_balance):
        self.client_id = client_id
        self.name = name
        self.beginning_balance = beginning_balance
        self.invoices = invoices
        self.receipts = receipts
        self.service_charges = service_charges
        self.adjustments = adjustments
        self.zero_to_thirty_days = zero_to_thirty_days
        self.thirty_to_sixty_days = thirty_to_sixty_days
        self.sixty_to_ninety_days = sixty_to_ninety_days
        self.ninety_to_one_hundred_twenty_days = ninety_to_one_hundred_twenty_days
        self.one_hundred_twenty_plus_days = one_hundred_twenty_plus_days
        self.ending_balance = ending_balance


class Client(Base):
    """
    Represents each individual client. Includes their contact info, as well
    as a history of how they have been contacted and what they have paid.
    """

    __tablename__ = "Client"

    client_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

    def __init__(self, client_id, name, email, phone):
        self.client_id = client_id
        self.name = name
        self.email = email
        self.phone = phone


class ContactHistory(Base):
    """
    Represents a complete history of how and when a client has been contacted
    since the start of service.

    The format of each 'history' type is...

        {contact_datetime: contact_type_identifier_string}

    ...where contact type identifiers refer to different iterations such as 
    'Email A', 'Email B', etc.
    """

    __tablename__ = "ContactHistory"

    client_id = Column(Integer, primary_key=True)
    email_history = Column(PickleType)
    text_history = Column(PickleType)
    call_history = Column(PickleType)
    payment_history = Column(PickleType)

    def __init__(self, client_id, email_history, text_history, call_history, payment_history):
        self.client_id = client_id
        self.email_history = email_history
        self.text_history = text_history
        self.call_history = call_history
        self.payment_history = payment_history


def db_init():

    # Connect with database via engine
    engine = create_engine('sqlite://', echo=True, future=True)

    # Create database from all classes
    Base.metadata.create_all(engine)

    return engine

