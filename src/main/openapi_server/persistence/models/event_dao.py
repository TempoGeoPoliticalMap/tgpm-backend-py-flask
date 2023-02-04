# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import List, Dict  # noqa: F401

# from openapi_server.persistence.models.country_dao import CountryDao
# from openapi_server.persistence.models.event_type import EventType
# from openapi_server.persistence.models.location_dao import LocationDao
from openapi_server import util


class EventDao:
    def __init__(
        self,
        type=None,
        wikidata_id=None,
        name=None,
        countries=None,
        locations=None,
        start_time=None,
        end_time=None,
    ):  # noqa: E501
        """EventDao

        :param type: The type of this Event.  # noqa: E501
        :type type: EventType
        :param wikidata_id: The wikidata_id of this Event.  # noqa: E501
        :type wikidata_id: str
        :param name: The name of this Event.  # noqa: E501
        :type name: str
        :param countries: The countries of this Event.  # noqa: E501
        :type countries: List[Country]
        :param locations: The locations of this Event.  # noqa: E501
        :type locations: List[Location]
        :param start_time: The start_time of this Event.  # noqa: E501
        :type start_time: datetime
        :param end_time: The end_time of this Event.  # noqa: E501
        :type end_time: datetime
        """
        self.openapi_types = {
            "type": EventType,
            "wikidata_id": str,
            "name": str,
            "countries": List[Country],
            "locations": List[Location],
            "start_time": datetime,
            "end_time": datetime,
        }

        self._type = type
        self._wikidata_id = wikidata_id
        self._name = name
        self._countries = countries
        self._locations = locations
        self._start_time = start_time
        self._end_time = end_time

    @classmethod
    def from_dict(cls, dikt) -> "Event":
        """Returns the dict as a models

        :param dikt: A dict.
        :type: dict
        :return: The Event of this Event.  # noqa: E501
        :rtype: Event
        """
        return util.deserialize_model(dikt, cls)

    @property
    def type(self):
        """Gets the type of this Event.


        :return: The type of this Event.
        :rtype: EventType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Event.


        :param type: The type of this Event.
        :type type: EventType
        """
        if type is None:
            raise ValueError(
                "Invalid value for `type`, must not be `None`"
            )  # noqa: E501

        self._type = type

    @property
    def wikidata_id(self):
        """Gets the wikidata_id of this Event.

        Record ID of a data item in https://www.wikidata.org.  # noqa: E501

        :return: The wikidata_id of this Event.
        :rtype: str
        """
        return self._wikidata_id

    @wikidata_id.setter
    def wikidata_id(self, wikidata_id):
        """Sets the wikidata_id of this Event.

        Record ID of a data item in https://www.wikidata.org.  # noqa: E501

        :param wikidata_id: The wikidata_id of this Event.
        :type wikidata_id: str
        """
        if wikidata_id is None:
            raise ValueError(
                "Invalid value for `wikidata_id`, must not be `None`"
            )  # noqa: E501

        self._wikidata_id = wikidata_id

    @property
    def name(self):
        """Gets the name of this Event.

        Name of a historical political Event.  # noqa: E501

        :return: The name of this Event.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Event.

        Name of a historical political Event.  # noqa: E501

        :param name: The name of this Event.
        :type name: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def countries(self):
        """Gets the countries of this Event.

        List of Countries related to the Event.  # noqa: E501

        :return: The countries of this Event.
        :rtype: List[Country]
        """
        return self._countries

    @countries.setter
    def countries(self, countries):
        """Sets the countries of this Event.

        List of Countries related to the Event.  # noqa: E501

        :param countries: The countries of this Event.
        :type countries: List[Country]
        """
        if countries is None:
            raise ValueError(
                "Invalid value for `countries`, must not be `None`"
            )  # noqa: E501
        if countries is not None and len(countries) > 200:
            raise ValueError(
                "Invalid value for `countries`, number of items must be less than or equal to `200`"
            )  # noqa: E501

        self._countries = countries

    @property
    def locations(self):
        """Gets the locations of this Event.

        List of Locations related to the Event.  # noqa: E501

        :return: The locations of this Event.
        :rtype: List[Location]
        """
        return self._locations

    @locations.setter
    def locations(self, locations):
        """Sets the locations of this Event.

        List of Locations related to the Event.  # noqa: E501

        :param locations: The locations of this Event.
        :type locations: List[Location]
        """
        if locations is not None and len(locations) > 200:
            raise ValueError(
                "Invalid value for `locations`, number of items must be less than or equal to `200`"
            )  # noqa: E501

        self._locations = locations

    @property
    def start_time(self):
        """Gets the start_time of this Event.

        Event timestamp; can be time or date, as well as month or year.  # noqa: E501

        :return: The start_time of this Event.
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this Event.

        Event timestamp; can be time or date, as well as month or year.  # noqa: E501

        :param start_time: The start_time of this Event.
        :type start_time: datetime
        """
        if start_time is None:
            raise ValueError(
                "Invalid value for `start_time`, must not be `None`"
            )  # noqa: E501

        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this Event.

        Event timestamp; can be time or date, as well as month or year.  # noqa: E501

        :return: The end_time of this Event.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this Event.

        Event timestamp; can be time or date, as well as month or year.  # noqa: E501

        :param end_time: The end_time of this Event.
        :type end_time: datetime
        """

        self._end_time = end_time
