# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Country(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, wikidata_id=None, name=None):  # noqa: E501
        """Country - a model defined in OpenAPI

        :param wikidata_id: The wikidata_id of this Country.  # noqa: E501
        :type wikidata_id: str
        :param name: The name of this Country.  # noqa: E501
        :type name: str
        """
        self.openapi_types = {
            'wikidata_id': str,
            'name': str
        }

        self.attribute_map = {
            'wikidata_id': 'wikidata-id',
            'name': 'name'
        }

        self._wikidata_id = wikidata_id
        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> 'Country':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Country of this Country.  # noqa: E501
        :rtype: Country
        """
        return util.deserialize_model(dikt, cls)

    @property
    def wikidata_id(self):
        """Gets the wikidata_id of this Country.

        Record ID of a data item in https://www.wikidata.org.  # noqa: E501

        :return: The wikidata_id of this Country.
        :rtype: str
        """
        return self._wikidata_id

    @wikidata_id.setter
    def wikidata_id(self, wikidata_id):
        """Sets the wikidata_id of this Country.

        Record ID of a data item in https://www.wikidata.org.  # noqa: E501

        :param wikidata_id: The wikidata_id of this Country.
        :type wikidata_id: str
        """

        self._wikidata_id = wikidata_id

    @property
    def name(self):
        """Gets the name of this Country.


        :return: The name of this Country.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Country.


        :param name: The name of this Country.
        :type name: str
        """

        self._name = name