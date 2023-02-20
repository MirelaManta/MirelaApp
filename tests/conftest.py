
import pytest
from website import create_app


@pytest.fixture()
def app():
    app = create_app(db_name="db_test.db")
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
