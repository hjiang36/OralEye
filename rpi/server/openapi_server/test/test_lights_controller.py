import unittest

from flask import json

from openapi_server.models.lights_blue_max_time_post_request import LightsBlueMaxTimePostRequest  # noqa: E501
from openapi_server.models.lights_control_post200_response import LightsControlPost200Response  # noqa: E501
from openapi_server.models.lights_status_get200_response import LightsStatusGet200Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestLightsController(BaseTestCase):
    """LightsController integration test stubs"""

    def test_lights_blue_max_time_post(self):
        """Test case for lights_blue_max_time_post

        Set blue light maximum on time for health safety
        """
        lights_blue_max_time_post_request = openapi_server.LightsBlueMaxTimePostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/lights/blue/max_time',
            method='POST',
            headers=headers,
            data=json.dumps(lights_blue_max_time_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lights_control_post(self):
        """Test case for lights_control_post

        Set lights on/off
        """
        lights_status_get200_response = openapi_server.LightsStatusGet200Response()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/lights/control',
            method='POST',
            headers=headers,
            data=json.dumps(lights_status_get200_response),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lights_status_get(self):
        """Test case for lights_status_get

        Get status of the lights
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/lights/status',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
