from typing import *

from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database.orm import start_mappers, metadata

_engine: Optional[Engine] = None
_mappers_started = False
_engine_is_test_db = False


def get_sessionmaker_for_engine():
    global _engine
    return sessionmaker(_engine)


def init_db(db_url):
    """
    Initializes the Database Engine and stores it globally.
    Starts ORM mapping after creating the Engine.

    :return:
    """
    global _engine

    _engine = create_engine(db_url)
    _start_mappers()

    return


def _start_mappers():
    global _mappers_started

    if _mappers_started is False:
        start_mappers()
        _mappers_started = True

    return


def create_db(engine_to_use, name: str):
    with engine_to_use.connect() as conn:
        conn.execute(text("COMMIT"))
        conn.execute(text(f"CREATE DATABASE {name}"))


def drop_db(engine_to_use, db_name: str):
    with engine_to_use.connect() as conn:
        conn.execute(text("COMMIT"))
        conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))


def create_test_database_url(url_to_modify: URL) -> URL:
    """
    Returns a modified URL where the database name is suffixed with _test
    :return:
    """
    return url_to_modify.set(database=url_to_modify.database + "_test")


def init_test_db(db_url: URL):
    """
    Connects to the configured database temporarily, issues CREATE commands to instantiate a test database,
    disposes the engine and replaces the global engine with the test one.
    :return:
    """
    global _engine
    global _engine_is_test_db

    temp_engine = create_engine(db_url)
    test_db_url = create_test_database_url(db_url)

    drop_db(temp_engine, test_db_url.database)
    create_db(temp_engine, test_db_url.database)

    _engine = create_engine(test_db_url)
    _engine_is_test_db = True

    metadata.create_all(_engine)
    _start_mappers()

    return


def destroy_test_db(db_url):
    """
    If the module's engine is a test engine, it will dispose it.
    Then, connects to the given db_url as "main" database and drops the test database.

    :param db_url:
    :return:
    """
    global _engine
    global _engine_is_test_db

    if _engine_is_test_db is True:
        _engine.dispose()

        temp_engine = create_engine(db_url)
        test_db_url = create_test_database_url(db_url)

        drop_db(temp_engine, test_db_url.database)

        _engine_is_test_db = False

    return

