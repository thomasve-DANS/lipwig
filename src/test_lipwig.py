from .main import app
from fastapi.testclient import TestClient
from unittest.mock import patch
from unittest import mock
import requests
import ast

client = TestClient(app)

@patch.object(requests, 'get')
def test_proxy(mockget):
    mockresponse = mock.MagicMock()
    mockresponse.text = 'example_text'
    mockresponse.json.return_value = 'none'
    mockrequest = mock.MagicMock()
    mockrequest.url = 'http://google.com'
    mockresponse.request = mockrequest
    mockget.return_value = mockresponse

    response = client.get('/proxy?url=http://google.com')
    content_str = response._content.decode('utf-8')
    content_dict = ast.literal_eval(content_str)
    assert content_dict.get('request_url') == 'http://google.com'
    assert response.status_code == 200
    assert content_dict.get('text') == 'example_text'
    assert mockget.called


def test_proxy_connectionerror():
    with mock.patch(
            'requests.get',
            side_effect=requests.exceptions.ConnectionError("Nope")
    ):

        response = client.get('/proxy?url=http://google')
        assert response.status_code == 418
