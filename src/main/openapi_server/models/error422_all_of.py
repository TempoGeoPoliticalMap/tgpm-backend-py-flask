# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Error422AllOf(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, status=None, title=None):  # noqa: E501
        """Error422AllOf - a model defined in OpenAPI

        :param status: The status of this Error422AllOf.  # noqa: E501
        :type status: object
        :param title: The title of this Error422AllOf.  # noqa: E501
        :type title: object
        """
        self.openapi_types = {
            'status': object,
            'title': object
        }

        self.attribute_map = {
            'status': 'status',
            'title': 'title'
        }

        self._status = status
        self._title = title

    @classmethod
    def from_dict(cls, dikt) -> 'Error422AllOf':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Error422_allOf of this Error422AllOf.  # noqa: E501
        :rtype: Error422AllOf
        """
        return util.deserialize_model(dikt, cls)

    @property
    def status(self):
        """Gets the status of this Error422AllOf.


        :return: The status of this Error422AllOf.
        :rtype: object
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Error422AllOf.


        :param status: The status of this Error422AllOf.
        :type status: object
        """

        self._status = status

    @property
    def title(self):
        """Gets the title of this Error422AllOf.


        :return: The title of this Error422AllOf.
        :rtype: object
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Error422AllOf.


        :param title: The title of this Error422AllOf.
        :type title: object
        """

        self._title = title
