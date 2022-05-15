# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.event import Event
from openapi_server import util

from openapi_server.models.event import Event  # noqa: E501


class EventListResponseBody(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, data=None):  # noqa: E501
        """EventListResponseBody - a models defined in OpenAPI

        :param data: The data of this EventListResponseBody.  # noqa: E501
        :type data: List[Event]
        """
        self.openapi_types = {
            'data': List[Event]
        }

        self.attribute_map = {
            'data': 'data'
        }

        self._data = data

    @classmethod
    def from_dict(cls, dikt) -> 'EventListResponseBody':
        """Returns the dict as a models

        :param dikt: A dict.
        :type: dict
        :return: The EventListResponseBody of this EventListResponseBody.  # noqa: E501
        :rtype: EventListResponseBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self):
        """Gets the data of this EventListResponseBody.


        :return: The data of this EventListResponseBody.
        :rtype: List[Event]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this EventListResponseBody.


        :param data: The data of this EventListResponseBody.
        :type data: List[Event]
        """
        if data is not None and len(data) > 10000:
            raise ValueError(
                "Invalid value for `data`, number of items must be less than or equal to `10000`")  # noqa: E501

        self._data = data
