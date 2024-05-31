import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.lights_blue_max_time_post_request import LightsBlueMaxTimePostRequest  # noqa: E501
from openapi_server.models.lights_control_post200_response import LightsControlPost200Response  # noqa: E501
from openapi_server.models.lights_status_get200_response import LightsStatusGet200Response  # noqa: E501
from openapi_server import util

from openapi_server.controllers.lights_controller_impl import set_light_status, get_light_status

def lights_blue_max_time_post(lights_blue_max_time_post_request):  # noqa: E501
    """Set blue light maximum on time for health safety

     # noqa: E501

    :param lights_blue_max_time_post_request: 
    :type lights_blue_max_time_post_request: dict | bytes

    :rtype: Union[LightsControlPost200Response, Tuple[LightsControlPost200Response, int], Tuple[LightsControlPost200Response, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        lights_blue_max_time_post_request = LightsBlueMaxTimePostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def lights_control_post(lights_status_get200_response):  # noqa: E501
    """Set lights on/off

     # noqa: E501

    :param lights_status_get200_response: 
    :type lights_status_get200_response: dict | bytes

    :rtype: Union[LightsControlPost200Response, Tuple[LightsControlPost200Response, int], Tuple[LightsControlPost200Response, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        lights_status_get200_response = LightsStatusGet200Response.from_dict(connexion.request.get_json())  # noqa: E501
    white_led = lights_status_get200_response.white_led
    blue_led = lights_status_get200_response.blue_led
    red_laser = lights_status_get200_response.red_laser

    set_light_status(white_led, blue_led, red_laser)

    return {"message": "Light statuses updated successfully"}, 200


def lights_status_get():  # noqa: E501
    """Get status of the lights

     # noqa: E501


    :rtype: Union[LightsStatusGet200Response, Tuple[LightsStatusGet200Response, int], Tuple[LightsStatusGet200Response, int, Dict[str, str]]
    """
    status = get_light_status()
    return status, 200
