from datetime import datetime
import pytest
import requests

from .TestConnexion import TestConnexion
from freezegun import freeze_time


@pytest.mark.usefixtures('client')
class TestRequest(TestConnexion):
    """A test to get events from the calendar api
    """

    def test_failOnUnknownRequestType(self, client):
        request = {
            'type': 'asdf',
            'payload': {
                'location':  'Stuttgart, de'
            }
        }

        response = client.post('api/v1/request', json=request)
        assert response.status_code == 404

    def test_getWeatherCurrent(self, client):
        request = {
            'type': 'weather_current',
            'payload': {
                'location':  'Stuttgart, de'
            }
        }

        response = client.post('api/v1/request', json=request)
        assert response.status_code == 200
        request = {
            'type': 'weather_current',
            'payload': {
                'location':  '04455, de'
            }
        }
        response = client.post('api/v1/request', json=request)
        assert response.status_code == 200

    @freeze_time("2019-04-01 10:00:00") # UTC Timestamp: 1554112800
    def test_getOutdatedForecast(self, client):
        request = {
            'type': 'weather_forecast',
            'payload': {
                'time': '1554111800',
                'location':  'Stuttgart, de'
            }
        }
        response = client.post('api/v1/request', json=request)

        assert response.status_code == 500

    @freeze_time("2019-04-01 10:00:00") # UTC Timestamp: 1554112800
    def test_getForecast(self, client):
        requestTime = 1554112900
        for i in range(5):
            request = {
                'type': 'weather_forecast',
                'payload': {
                    'time': str(requestTime),
                    'location':  'Stuttgart, de'
                }
            }
            response = client.post('api/v1/request', json=request)
            assert response.status_code == 200
            assert int(response.json[0]['payload']['data']['dt']) < requestTime or i == 0
            requestTime+= 1000
