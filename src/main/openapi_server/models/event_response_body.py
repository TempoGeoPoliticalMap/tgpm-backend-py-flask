# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import List, Dict  # noqa: F401

from openapi_server import util
from openapi_server.models.base_model_ import Model
from openapi_server.models.event import Event  # noqa: E501


class EventResponseBody(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, data=None):  # noqa: E501
        """EventResponseBody - a model defined in OpenAPI

        :param data: The data of this EventResponseBody.  # noqa: E501
        :type data: Event
        """
        self.openapi_types = {"data": Event}

        self.attribute_map = {"data": "data"}

        self._data = data

    @classmethod
    def from_dict(cls, dikt) -> "EventResponseBody":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EventResponseBody of this EventResponseBody.  # noqa: E501
        :rtype: EventResponseBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self):
        """Gets the data of this EventResponseBody.


        :return: The data of this EventResponseBody.
        :rtype: Event
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this EventResponseBody.


        :param data: The data of this EventResponseBody.
        :type data: Event
        """

        self._data = data
