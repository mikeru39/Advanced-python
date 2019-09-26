import pytest
from datetime import datetime
from protocol import make_response

CODE = 200
ACTION = 'test'
TIME = datetime.now().timestamp()
DATA = 'some client data'
REQUEST = {
    'action': ACTION,
    'time': TIME,
    'data': DATA
}
RESPONSE = {
    'action': ACTION,
    'time': TIME,
    'code': CODE,
    'data': DATA
}


def test_action_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    action = response.get('action')
    assert action == ACTION


def test_code_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    code = response.get('code')
    assert code == CODE


def test_time_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    time = response.get('time')
    assert time == TIME


def test_data_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    data = response.get('data')
    assert data == DATA


def test_invalid_make_response():
    with pytest.raises(AttributeError):
        response = make_response(None, CODE)
