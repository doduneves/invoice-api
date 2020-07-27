import os
import tempfile

import pytest

from app import app
from config import db_connect

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db_connect.connect_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_api_without_token(client):
    res = client.get('/invoices/')
    result_json = res.get_json()
    assert 'message' in result_json
    assert result_json['message'] == 'Access Denied'


def test_invoices_list_keys(client):
    res = client.get('/invoices/', headers = {'Auth-Key':'822e75ef88572e1278a74621385280ec'})
    result_json = res.get_json()
    assert '_links' in result_json
    assert 'invoices' in result_json

