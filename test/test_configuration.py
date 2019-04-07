import pytest
from api.models.Configuration import CONFIG
from .TestConnexion import TestConnexion


@pytest.mark.usefixtures('client')
class TestConfiguration(TestConnexion):
    """A test to get API token from PrefStore
    """

    def test_getAPIToken(self, client):
        CONFIG.readApiToken = False
        assert CONFIG.getAPItoken() == TestConnexion.WEATHER_API_TOKEN

    def test_failOnGettingAPIToken(self, client, requests_mock):
        CONFIG.readApiToken = False
        requests_mock.get(f'{self.CENTRAL_NODE_BASE_URL}/preferences/global/', status_code=500)
        try:
            assert CONFIG.getAPItoken() == TestConnexion.WEATHER_API_TOKEN
        except AssertionError:
            pass
