import unittest

from flask import json

from openapi_server.models.camera_autofocus_post_request import CameraAutofocusPostRequest  # noqa: E501
from openapi_server.models.camera_capture_post200_response import CameraCapturePost200Response  # noqa: E501
from openapi_server.models.camera_exposure_post_request import CameraExposurePostRequest  # noqa: E501
from openapi_server.models.camera_manual_focus_post_request import CameraManualFocusPostRequest  # noqa: E501
from openapi_server.models.lights_control_post200_response import LightsControlPost200Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestCameraController(BaseTestCase):
    """CameraController integration test stubs"""

    def test_camera_autofocus_post(self):
        """Test case for camera_autofocus_post

        Set auto-focus on/off
        """
        camera_autofocus_post_request = openapi_server.CameraAutofocusPostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/camera/autofocus',
            method='POST',
            headers=headers,
            data=json.dumps(camera_autofocus_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_camera_capture_post(self):
        """Test case for camera_capture_post

        Capture raw image
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/camera/capture',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_camera_exposure_post(self):
        """Test case for camera_exposure_post

        Set exposure time
        """
        camera_exposure_post_request = openapi_server.CameraExposurePostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/camera/exposure',
            method='POST',
            headers=headers,
            data=json.dumps(camera_exposure_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_camera_manual_focus_post(self):
        """Test case for camera_manual_focus_post

        Set manual focus distance
        """
        camera_manual_focus_post_request = openapi_server.CameraManualFocusPostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/camera/manual_focus',
            method='POST',
            headers=headers,
            data=json.dumps(camera_manual_focus_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_camera_preview_start_post(self):
        """Test case for camera_preview_start_post

        Start camera preview
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/camera/preview/start',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_camera_preview_stop_post(self):
        """Test case for camera_preview_stop_post

        Stop camera preview
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/camera/preview/stop',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
