from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class CameraMetadataGet200Response(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, job_id=None, light=None, timestamp=None, other_metadata=None):  # noqa: E501
        """CameraMetadataGet200Response - a model defined in OpenAPI

        :param job_id: The job_id of this CameraMetadataGet200Response.  # noqa: E501
        :type job_id: str
        :param light: The light of this CameraMetadataGet200Response.  # noqa: E501
        :type light: str
        :param timestamp: The timestamp of this CameraMetadataGet200Response.  # noqa: E501
        :type timestamp: datetime
        :param other_metadata: The other_metadata of this CameraMetadataGet200Response.  # noqa: E501
        :type other_metadata: Dict[str, str]
        """
        self.openapi_types = {
            'job_id': str,
            'light': str,
            'timestamp': datetime,
            'other_metadata': Dict[str, str]
        }

        self.attribute_map = {
            'job_id': 'job_id',
            'light': 'light',
            'timestamp': 'timestamp',
            'other_metadata': 'other_metadata'
        }

        self._job_id = job_id
        self._light = light
        self._timestamp = timestamp
        self._other_metadata = other_metadata

    @classmethod
    def from_dict(cls, dikt) -> 'CameraMetadataGet200Response':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _camera_metadata_get_200_response of this CameraMetadataGet200Response.  # noqa: E501
        :rtype: CameraMetadataGet200Response
        """
        return util.deserialize_model(dikt, cls)

    @property
    def job_id(self) -> str:
        """Gets the job_id of this CameraMetadataGet200Response.


        :return: The job_id of this CameraMetadataGet200Response.
        :rtype: str
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id: str):
        """Sets the job_id of this CameraMetadataGet200Response.


        :param job_id: The job_id of this CameraMetadataGet200Response.
        :type job_id: str
        """

        self._job_id = job_id

    @property
    def light(self) -> str:
        """Gets the light of this CameraMetadataGet200Response.


        :return: The light of this CameraMetadataGet200Response.
        :rtype: str
        """
        return self._light

    @light.setter
    def light(self, light: str):
        """Sets the light of this CameraMetadataGet200Response.


        :param light: The light of this CameraMetadataGet200Response.
        :type light: str
        """
        allowed_values = ["ambient", "white", "blue"]  # noqa: E501
        if light not in allowed_values:
            raise ValueError(
                "Invalid value for `light` ({0}), must be one of {1}"
                .format(light, allowed_values)
            )

        self._light = light

    @property
    def timestamp(self) -> datetime:
        """Gets the timestamp of this CameraMetadataGet200Response.


        :return: The timestamp of this CameraMetadataGet200Response.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        """Sets the timestamp of this CameraMetadataGet200Response.


        :param timestamp: The timestamp of this CameraMetadataGet200Response.
        :type timestamp: datetime
        """

        self._timestamp = timestamp

    @property
    def other_metadata(self) -> Dict[str, str]:
        """Gets the other_metadata of this CameraMetadataGet200Response.


        :return: The other_metadata of this CameraMetadataGet200Response.
        :rtype: Dict[str, str]
        """
        return self._other_metadata

    @other_metadata.setter
    def other_metadata(self, other_metadata: Dict[str, str]):
        """Sets the other_metadata of this CameraMetadataGet200Response.


        :param other_metadata: The other_metadata of this CameraMetadataGet200Response.
        :type other_metadata: Dict[str, str]
        """

        self._other_metadata = other_metadata
