# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import List, Dict  # noqa: F401

from openapi_server import util
from openapi_server.models.base_model_ import Model


class BasicErrorObject(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, code=None, detail=None, source=None):  # noqa: E501
        """BasicErrorObject - a model defined in OpenAPI

        :param id: The id of this BasicErrorObject.  # noqa: E501
        :type id: str
        :param code: The code of this BasicErrorObject.  # noqa: E501
        :type code: int
        :param detail: The detail of this BasicErrorObject.  # noqa: E501
        :type detail: str
        :param source: The source of this BasicErrorObject.  # noqa: E501
        :type source: str
        """
        self.openapi_types = {"id": str, "code": int, "detail": str, "source": str}

        self.attribute_map = {
            "id": "id",
            "code": "code",
            "detail": "detail",
            "source": "source",
        }

        self._id = id
        self._code = code
        self._detail = detail
        self._source = source

    @classmethod
    def from_dict(cls, dikt) -> "BasicErrorObject":
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The BasicErrorObject of this BasicErrorObject.  # noqa: E501
        :rtype: BasicErrorObject
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this BasicErrorObject.


        :return: The id of this BasicErrorObject.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BasicErrorObject.


        :param id: The id of this BasicErrorObject.
        :type id: str
        """

        self._id = id

    @property
    def code(self):
        """Gets the code of this BasicErrorObject.

        An application-specific error code, expressed as a string value.  # noqa: E501

        :return: The code of this BasicErrorObject.
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this BasicErrorObject.

        An application-specific error code, expressed as a string value.  # noqa: E501

        :param code: The code of this BasicErrorObject.
        :type code: int
        """

        self._code = code

    @property
    def detail(self):
        """Gets the detail of this BasicErrorObject.

        A human-readable explanation specific to this occurrence of the problem.  # noqa: E501

        :return: The detail of this BasicErrorObject.
        :rtype: str
        """
        return self._detail

    @detail.setter
    def detail(self, detail):
        """Sets the detail of this BasicErrorObject.

        A human-readable explanation specific to this occurrence of the problem.  # noqa: E501

        :param detail: The detail of this BasicErrorObject.
        :type detail: str
        """

        self._detail = detail

    @property
    def source(self):
        """Gets the source of this BasicErrorObject.

        An object containing references to the source of the error.  # noqa: E501

        :return: The source of this BasicErrorObject.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this BasicErrorObject.

        An object containing references to the source of the error.  # noqa: E501

        :param source: The source of this BasicErrorObject.
        :type source: str
        """

        self._source = source
