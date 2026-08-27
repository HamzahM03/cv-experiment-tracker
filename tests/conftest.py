import os
from urllib.parse import urlparse, urlunparse

from dotenv import load_dotenv

load_dotenv()

_dev_url = os.environ["DATABASE_URL"]
_parsed = urlparse(_dev_url)
_dev_db_name = _parsed.path.lstrip("/")
_test_db_name = f"{_dev_db_name}_test"

assert _parsed.hostname in ("localhost", "127.0.0.1"), (
    f"Refusing to run: host {_parsed.hostname!r} is not localhost/127.0.0.1"
)
assert _test_db_name.endswith("_test"), (
    f"Refusing to run: resolved DATABASE_URL {_test_db_name!r} does not end in '_test'"
)
assert _test_db_name != _dev_db_name, (
    "Refusing to run: test DB name must differ from the dev DB name"
)
assert _test_db_name == "cv_experiment_tracker_test", (
    f"Refusing to run: unexpected test DB name {_test_db_name!r}"
)

# Must happen before any `app.*` import, since app.db.database creates its
# engine from DATABASE_URL at import time.
os.environ["DATABASE_URL"] = urlunparse(_parsed._replace(path=f"/{_test_db_name}"))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.database import Base, engine
from app.db.dependencies import get_db
from app.main import app

# Importing app.main pulls in every router -> service -> repository, and each
# repository imports its model module directly, which is what registers each
# model's table on Base.metadata. Assert that actually happened before we
# create the schema, so a missing import fails loudly instead of silently
# skipping a table.
_expected_tables = {"projects", "datasets", "images", "experiments"}
_missing_tables = _expected_tables - set(Base.metadata.tables)
assert not _missing_tables, (
    f"Refusing to run: models not registered in Base.metadata: {_missing_tables}"
)


@pytest.fixture(scope="session", autouse=True)
def _setup_test_schema():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    def _get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
