import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps
from roux.algo.geneweaver.kargers.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def inject_db_session_for_celery(func):
    """
    This is a decorator to handle adding a database dependency injection to a celery task method
    call that has bind=True set.
    This method handles creating a session, adding it to kwargs['db'], and closing the session when
    the method completes.
    :param func: The func to decorate
    :return: The decorated func
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        db = None
        try:
            db = SessionLocal()
            logging.info("Initialized database connection")
            kwargs['db'] = db
            func(self, *args, **kwargs)
        finally:
            if db:
                logging.info("Closing database connection")
                db.close()
    return wrapper


def inject_db_session(func):
    """
    This is a decorator to handle adding a database dependency injection to a method call. This
    method handles creating a session, adding it to kwargs['db'], and closing the session when
    the method completes.
    :param func: The func to decorate
    :return: The decorated func
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = None
        try:
            db = SessionLocal()
            logging.info("Initialized database connection")
            kwargs['db'] = db
            func(*args, **kwargs)
        finally:
            if db:
                logging.info("Closing database connection")
                db.close()
    return wrapper
