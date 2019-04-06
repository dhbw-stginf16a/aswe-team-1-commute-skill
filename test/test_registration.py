#!/usr/bin/env python3

import time

from api.models.RegistrationThread import RegistrationThread

class TestRegistration:
    centralNode = 'http://localhost:8080/api/v1'
    url = 'http://localhost:5000/api/v1'


    def test_retry(self):
        reg = RegistrationThread(self.centralNode, self.url)

        reg.start()
        # Wait for the thread to fail at least once
        time.sleep(3)
        reg.stop()

    def test_success(self, requests_mock):
        requests_mock.post(f'{self.centralNode}/monitoring', text='', status_code=204)
        reg = RegistrationThread(self.centralNode, self.url)

        reg.start()
        # Wait for the thread to fail at least once
        reg.stop()