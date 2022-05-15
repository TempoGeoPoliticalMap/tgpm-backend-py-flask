# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.basic_error_object import BasicErrorObject
from openapi_server.models.error409_all_of import Error409AllOf
from openapi_server import util

from openapi_server.models.basic_error_object import BasicErrorObject  # noqa: E501
from openapi_server.models.error409_all_of import Error409AllOf  # noqa: E501


class Error409(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, status=None, code=None, title=None, detail=None, source=None):  # noqa: E501
        """Error409 - a model defined in OpenAPI

        :param id: The id of this Error409.  # noqa: E501
        :type id: str
        :param status: The status of this Error409.  # noqa: E501
        :type status: object
        :param code: The code of this Error409.  # noqa: E501
        :type code: int
        :param title: The title of this Error409.  # noqa: E501
        :type title: object
        :param detail: The detail of this Error409.  # noqa: E501
        :type detail: str
        :param source: The source of this Error409.  # noqa: E501
        :type source: str
        """
        self.openapi_types = {
            'id': str,
            'status': object,
            'code': int,
            'title': object,
            'detail': str,
            'source': str
        }

        self.attribute_map = {
            'id': 'id',
            'status': 'status',
            'code': 'code',
            'title': 'title',
            'detail': 'detail',
            'source': 'source'
        }

        self._id = id
        self._status = status
        self._code = code
        self._title = title
        self._detail = detail
        self._source = source

    @classmethod
    def from_dict(cls, dikt) -> 'Error409':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Error409 of this Error409.  # noqa: E501
        :rtype: Error409
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Error409.


        :return: The id of this Error409.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Error409.


        :param id: The id of this Error409.
        :type id: str
        """

        self._id = id

    @property
    def status(self):
        """Gets the status of this Error409.


        :return: The status of this Error409.
        :rtype: object
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Error409.


        :param status: The status of this Error409.
        :type status: object
        """

        self._status = status

    @property
    def code(self):
        """Gets the code of this Error409.

        An application-specific error code, expressed as a string value.  # noqa: E501

        :return: The code of this Error409.
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this Error409.

        An application-specific error code, expressed as a string value.  # noqa: E501

        :param code: The code of this Error409.
        :type code: int
        """

        self._code = code

    @property
    def title(self):
        """Gets the title of this Error409.


        :return: The title of this Error409.
        :rtype: object
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Error409.


        :param title: The title of this Error409.
        :type title: object
        """

        self._title = title

    @property
    def detail(self):
        """Gets the detail of this Error409.

        A human-readable explanation specific to this occurrence of the problem.  # noqa: E501

        :return: The detail of this Error409.
        :rtype: str
        """
        return self._detail

    @detail.setter
    def detail(self, detail):
        """Sets the detail of this Error409.

        A human-readable explanation specific to this occurrence of the problem.  # noqa: E501

        :param detail: The detail of this Error409.
        :type detail: str
        """

        self._detail = detail

    @property
    def source(self):
        """Gets the source of this Error409.

        An object containing references to the source of the error.  # noqa: E501

        :return: The source of this Error409.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this Error409.

        An object containing references to the source of the error.  # noqa: E501

        :param source: The source of this Error409.
        :type source: str
        """

        self._source = source