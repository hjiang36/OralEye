from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class LightsStatusGet200Response(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, white_led=None, blue_led=None, red_laser=None):  # noqa: E501
        """LightsStatusGet200Response - a model defined in OpenAPI

        :param white_led: The white_led of this LightsStatusGet200Response.  # noqa: E501
        :type white_led: str
        :param blue_led: The blue_led of this LightsStatusGet200Response.  # noqa: E501
        :type blue_led: str
        :param red_laser: The red_laser of this LightsStatusGet200Response.  # noqa: E501
        :type red_laser: str
        """
        self.openapi_types = {
            'white_led': str,
            'blue_led': str,
            'red_laser': str
        }

        self.attribute_map = {
            'white_led': 'white_led',
            'blue_led': 'blue_led',
            'red_laser': 'red_laser'
        }

        self._white_led = white_led
        self._blue_led = blue_led
        self._red_laser = red_laser

    @classmethod
    def from_dict(cls, dikt) -> 'LightsStatusGet200Response':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _lights_status_get_200_response of this LightsStatusGet200Response.  # noqa: E501
        :rtype: LightsStatusGet200Response
        """
        return util.deserialize_model(dikt, cls)

    @property
    def white_led(self) -> str:
        """Gets the white_led of this LightsStatusGet200Response.


        :return: The white_led of this LightsStatusGet200Response.
        :rtype: str
        """
        return self._white_led

    @white_led.setter
    def white_led(self, white_led: str):
        """Sets the white_led of this LightsStatusGet200Response.


        :param white_led: The white_led of this LightsStatusGet200Response.
        :type white_led: str
        """
        allowed_values = ["on", "off"]  # noqa: E501
        if white_led not in allowed_values:
            raise ValueError(
                "Invalid value for `white_led` ({0}), must be one of {1}"
                .format(white_led, allowed_values)
            )

        self._white_led = white_led

    @property
    def blue_led(self) -> str:
        """Gets the blue_led of this LightsStatusGet200Response.


        :return: The blue_led of this LightsStatusGet200Response.
        :rtype: str
        """
        return self._blue_led

    @blue_led.setter
    def blue_led(self, blue_led: str):
        """Sets the blue_led of this LightsStatusGet200Response.


        :param blue_led: The blue_led of this LightsStatusGet200Response.
        :type blue_led: str
        """
        allowed_values = ["on", "off"]  # noqa: E501
        if blue_led not in allowed_values:
            raise ValueError(
                "Invalid value for `blue_led` ({0}), must be one of {1}"
                .format(blue_led, allowed_values)
            )

        self._blue_led = blue_led

    @property
    def red_laser(self) -> str:
        """Gets the red_laser of this LightsStatusGet200Response.


        :return: The red_laser of this LightsStatusGet200Response.
        :rtype: str
        """
        return self._red_laser

    @red_laser.setter
    def red_laser(self, red_laser: str):
        """Sets the red_laser of this LightsStatusGet200Response.


        :param red_laser: The red_laser of this LightsStatusGet200Response.
        :type red_laser: str
        """
        allowed_values = ["on", "off"]  # noqa: E501
        if red_laser not in allowed_values:
            raise ValueError(
                "Invalid value for `red_laser` ({0}), must be one of {1}"
                .format(red_laser, allowed_values)
            )

        self._red_laser = red_laser
