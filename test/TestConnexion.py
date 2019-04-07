import pytest
import os

from app import app


class TestConnexion:
    """The base test providing auth and flask clients to other tests
    """
    cache: dict = {}
    CENTRAL_NODE_BASE_URL = os.environ.setdefault('CENTRAL_NODE_BASE_URL', 'http://localhost:8080/api/v1')

    @pytest.fixture(scope='function')
    def client(self, requests_mock):
        weatherApi = {
            "dummy": "dummy"
        }

        forecastStuff = {
            "list":[
                {
                    "dt": "1554113800"
                },
                {
                    "dt": "1554114800"
                },
                {
                    "dt": "1554115800"
                },
                {
                    "dt": "1554116800"
                }
            ]
        }

        requests_mock.get(f'{self.CENTRAL_NODE_BASE_URL}/preferences/global/', status_code=200, json=globalPrefs)
        requests_mock.get(f'https://api.openweathermap.org/data/2.5/weather', status_code=200, json=weatherApi)
        requests_mock.get(f'https://api.openweathermap.org/data/2.5/forecast', status_code=200, json=forecastStuff)
        requests_mock.post(f'{self.CENTRAL_NODE_BASE_URL}/monitoring', text='', status_code=204)
        with app.app.test_client() as c:
            yield c
            app.registerThread.stop()
