# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class EventType(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    WARFARE_AND_ARMED_CONFLICTS = "WARFARE_AND_ARMED_CONFLICTS"

    def __init__(self):  # noqa: E501
        """EventType - a model defined in OpenAPI"""
        self.openapi_types = {}

        self.attribute_map = {}

    @classmethod
    def from_dict(cls, dikt) -> "EventType":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EventType of this EventType.  # noqa: E501
        :rtype: EventType
        """
        return util.deserialize_model(dikt, cls)
