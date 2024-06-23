import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.camera_autofocus_post_request import CameraAutofocusPostRequest  # noqa: E501
from openapi_server.models.camera_exposure_post_request import CameraExposurePostRequest  # noqa: E501
from openapi_server.models.camera_manual_focus_post_request import CameraManualFocusPostRequest  # noqa: E501
from openapi_server.models.camera_metadata_get200_response import CameraMetadataGet200Response  # noqa: E501
from openapi_server.models.lights_control_post200_response import LightsControlPost200Response  # noqa: E501
from openapi_server import util

from openapi_server.controllers.camera_controller_impl import (
    camera_preview_start_impl,
    camera_preview_stop_impl,
    camera_preview_video_feed_get_impl,
    camera_autofocus_post_impl,
    camera_exposure_post_impl,
    camera_manual_focus_post_impl,
    camera_capture_post_impl,
    camera_metadata_get_impl,
)


def camera_autofocus_post():  # noqa: E501
    """Set auto-focus on/off

     # noqa: E501

    :param camera_autofocus_post_request: 
    :type camera_autofocus_post_request: dict | bytes

    :rtype: Union[LightsControlPost200Response, Tuple[LightsControlPost200Response, int], Tuple[LightsControlPost200Response, int, Dict[str, str]]
    """
    camera_autofocus_post_request = CameraAutofocusPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return camera_autofocus_post_impl(camera_autofocus_post_request.autofocus)


def camera_capture_post():  # noqa: E501
    """Capture raw image

     # noqa: E501


    :rtype: Union[file, Tuple[file, int], Tuple[file, int, Dict[str, str]]
    """
    return camera_capture_post_impl()


def camera_exposure_post():  # noqa: E501
    """Set exposure time

     # noqa: E501

    :param camera_exposure_post_request: 
    :type camera_exposure_post_request: dict | bytes

    :rtype: Union[LightsControlPost200Response, Tuple[LightsControlPost200Response, int], Tuple[LightsControlPost200Response, int, Dict[str, str]]
    """
    camera_exposure_post_request = CameraExposurePostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return camera_exposure_post_impl(camera_exposure_post_request.exposure_time)


def camera_manual_focus_post():  # noqa: E501
    """Set manual focus distance

     # noqa: E501

    :param camera_manual_focus_post_request: 
    :type camera_manual_focus_post_request: dict | bytes

    :rtype: Union[LightsControlPost200Response, Tuple[LightsControlPost200Response, int], Tuple[LightsControlPost200Response, int, Dict[str, str]]
    """
    camera_manual_focus_post_request = CameraManualFocusPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return camera_manual_focus_post_impl(camera_manual_focus_post_request.focus_distance)


def camera_metadata_get(job_id, light):  # noqa: E501
    """Retrieve metadata of a capture

     # noqa: E501

    :param job_id: 
    :type job_id: str
    :type job_id: str
    :param light: 
    :type light: str

    :rtype: Union[CameraMetadataGet200Response, Tuple[CameraMetadataGet200Response, int], Tuple[CameraMetadataGet200Response, int, Dict[str, str]]
    """
    return camera_metadata_get_impl(job_id, light)


def camera_preview_start_post():  # noqa: E501
    """Start camera preview

     # noqa: E501


    :rtype: Union[LightsControlPost200Response, Tuple[LightsControlPost200Response, int], Tuple[LightsControlPost200Response, int, Dict[str, str]]
    """
    return camera_preview_start_impl()


def camera_preview_stop_post():  # noqa: E501
    """Stop camera preview

     # noqa: E501


    :rtype: Union[LightsControlPost200Response, Tuple[LightsControlPost200Response, int], Tuple[LightsControlPost200Response, int, Dict[str, str]]
    """
    return camera_preview_stop_impl()


def camera_preview_video_feed_get():  # noqa: E501
    """Get MJPEG video feed

    Streams MJPEG video feed from the camera # noqa: E501


    :rtype: Union[file, Tuple[file, int], Tuple[file, int, Dict[str, str]]
    """
    return camera_preview_video_feed_get_impl()
