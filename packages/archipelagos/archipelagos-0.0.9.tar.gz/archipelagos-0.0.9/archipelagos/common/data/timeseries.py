"""
Classes and functions related to time-series.
"""
from __future__ import annotations

from archipelagos.common.data import get_secs_from_timestamp, get_nanos_from_timestamp, get_timestamp
from archipelagos.common.data import get_yyyy_mm_dd_hh_mm_ss_n
from archipelagos.common.protobuf.common.data.timeseries import TimeSeriesMetadata_pb2, TimeSeriesData_pb2
from archipelagos.common.protobuf.common.data.timeseries import TimeSeriesMetadataRequest_pb2, TimeSeries_pb2
from archipelagos.common.protobuf.common.data.timeseries import TimeSeriesRequest_pb2, TimeSeriesResponse_pb2
from archipelagos.common.protobuf.common.data.timeseries import TimeSeriesMetadataResponse_pb2
from archipelagos.common.protobuf.common.data import DataEntry_pb2
from archipelagos.common.protobuf.common import Timestamp_pb2
from archipelagos.common.data import _valid_feature_value, _feature_value_equals
from archipelagos.common.data import _get_feature_value, _get_feature_value_from_proto
from archipelagos.common.data import Frequency, is_valid_token
from archipelagos.common.platform import ClientType

import array
from typing import Dict, List, Tuple, Any
from datetime import datetime, date
from pandas import Timestamp


class TimeSeriesMetadata:
    """
    Represents the metadata about a time-series.
    """
    def __init__(self,
                 source: str,
                 code: str,
                 ts_id: str,
                 url: str,
                 summary: str,
                 description: str,
                 features: Dict[str, str],
                 frequency: Frequency,
                 properties: Dict[str, str],
                 premium: bool,
                 created: Timestamp,
                 edited: Timestamp = None,
                 refreshed: Timestamp = None,
                 oldest_timestamp: Timestamp = None,
                 newest_timestamp: Timestamp = None):
        """
        All parameters should be supplied unless deserializing an object.

        :param source: The source for the time-series.
        :type source: str

        :param code: The code for the time-series.
        :type code: str

        :param ts_id: The ID for the time-series.
        :type ts_id: str

        :param url: The URL for the time-series.
        :type url:

        :param summary: The summary for the time-series.
        :type summary: str

        :param description: The description for the time-series.
        :type description: str

        :param features: Dict[str, str]
        :type features: The time-series' features and their descriptions.

        :param frequency: The frequency of the time-series.
        :type frequency: Frequency

        :param properties: The time-series' properties.
        :type properties: Dict[str, str]

        :param premium: True if the time-series is premium, False otherwise.
        :type premium: bool

        :param created: When (in UTC) the time-series was created.
        :type created: Timestamp

        :param edited: When (in UTC) the metadata for the time-series was last edited.
        :type edited: Timestamp

        :param refreshed: When (in UTC) the data in the time-series was last refreshed; can be None if no data has yet been entered.
        :type refreshed: Timestamp

        :param oldest_timestamp: The oldest date/time in the associated time-series; can be None if the time-series is empty.
        :type oldest_timestamp: Timestamp

        :param newest_timestamp: The newest date/time in the associated time-series; can be None if the time-series is empty.
        :type newest_timestamp: Timestamp
        """
        # Check if the data is valid

        if not isinstance(source, str):
            raise ValueError("source is not a valid str")

        if not is_valid_token(source):
            raise ValueError("source is not valid")

        if not isinstance(code, str):
            raise ValueError("code is not a valid str")

        if not is_valid_token(code):
            raise ValueError("code is not valid")

        if not isinstance(ts_id, str):
            raise ValueError("ts_id is not a valid str")

        if not is_valid_token(ts_id):
            raise ValueError("ts_id is not valid")

        if not isinstance(url, str):
            raise ValueError("url is not a valid str")

        if not isinstance(summary, str):
            raise ValueError("summary is not a valid str")

        if not isinstance(description, str):
            raise ValueError("description is not a valid str")

        if not isinstance(features, dict):
            raise ValueError("features is not a valid dict")
        else:
            for key, value in features.items():
                if not isinstance(key, str):
                    raise ValueError("features should contain instances of str")
                elif not is_valid_token(key):
                    raise ValueError("\"{}\" is not a valid name for a feature".format(key))

                if not isinstance(value, str):
                    raise ValueError("features should contain instances of str")

        if not isinstance(properties, dict):
            raise ValueError("properties is not a valid dict")
        else:
            for key, value in properties.items():
                if not isinstance(key, str):
                    raise ValueError("properties should contain instances of str")
                elif not is_valid_token(key):
                    raise ValueError("\"{}\" is not a valid name for a property".format(key))

                if not isinstance(value, str):
                    raise ValueError("properties should contain instances of str")

        if not isinstance(frequency, Frequency):
            raise ValueError("frequency is not a valid Frequency")

        if not isinstance(premium, bool):
            raise ValueError("restricted is not a valid bool")

        if not isinstance(created, Timestamp):
            raise ValueError("created is not a valid Timestamp")

        if edited is None:
            edited = created
        elif not isinstance(edited, Timestamp):
            raise ValueError("edited is not a valid Timestamp")

        if edited < created:
            raise ValueError("edited is before created")

        if refreshed is None and (oldest_timestamp is not None or newest_timestamp is not None):
            raise ValueError("refreshed is None but either oldest_date_time or newest_date_time is not")

        if oldest_timestamp is not None and newest_timestamp is None:
            raise ValueError("oldest_date_time is not None but newest_date_time is")

        if oldest_timestamp is None and newest_timestamp is not None:
            raise ValueError("newest_date_time is not None but oldest_date_time is")

        if oldest_timestamp is not None and newest_timestamp is not None:
            if newest_timestamp < oldest_timestamp:
                raise ValueError("newest_date_time is before oldest_date_time")

        if refreshed is not None and refreshed < created:
            raise ValueError("refreshed is before created")

        # Store the data

        self._source = source
        self._code = code
        self._ts_id = ts_id
        self._url = url
        self._summary = summary
        self._description = description
        self._features = features
        self._frequency = frequency
        self._properties = properties
        self._premium = premium
        self._created = created
        self._edited = edited
        self._refreshed = refreshed
        self._oldest_date_time = oldest_timestamp
        self._newest_date_time = newest_timestamp

        self._build_hash_code()

    def _build_hash_code(self):
        """
        Calculates and caches the hash code associated with this.
        """
        prime = 31
        result = 1

        result = prime * result + hash(self._source) if self._source is not None else 0
        result = prime * result + hash(self._code) if self._code is not None else 0
        result = prime * result + hash(self._ts_id) if self._ts_id is not None else 0

        self._hash_code = result

    @property
    def source(self) -> str:
        """
        Returns the source for the time-series.

        :return: The source for the time-series.
        :rtype: str
        """
        return self._source

    @property
    def code(self) -> str:
        """
        Returns the code for the time-series.

        :return: The code for the time-series.
        :rtype: str
        """
        return self._code

    @property
    def ts_id(self) -> str:
        """
        Returns the ID for the time-series.

        :return: The ID for the time-series.
        :rtype: str
        """
        return self._ts_id

    @property
    def url(self) -> str:
        """
        Returns the url for the time-series.

        :return: The url for the time-series.
        :rtype: str
        """
        return self._url

    @property
    def summary(self) -> str:
        """
        Returns the summary for the time-series.

        :return: The summary for the time-series.
        :rtype: str
        """
        return self._summary

    @property
    def description(self) -> str:
        """
        Returns the description for the time-series.

        :return: The description for the time-series.
        :rtype: str
        """
        return self._description

    @property
    def features(self) -> Dict[str, str]:
        """
        Returns the time-series' features and their descriptions.

        :return: The time-series' features and their descriptions.
        :rtype: Dict[str, str]
        """
        return self._features

    @property
    def frequency(self) -> Frequency:
        """
        Returns the frequency of the time-series.

        :return: The frequency of the time-series.
        :rtype: Frequency
        """
        return self._frequency

    @property
    def properties(self) -> Dict[str, str]:
        """
        Returns the time-series' properties.

        :return: The time-series' properties.
        :rtype: Dict[str, str]
        """
        return self._properties

    @property
    def premium(self) -> bool:
        """
        Returns True if the time-series is premium, False otherwise.

        :return: True if the time-series is premium, False otherwise.
        :rtype: bool
        """
        return self._premium

    @property
    def created(self) -> Timestamp:
        """
        Returns when (in UTC) the time-series was created.

        :return: When (in UTC) the time-series was created.
        :rtype: Timestamp
        """
        return self._created

    @property
    def edited(self) -> Timestamp:
        """
        Returns when (in UTC) the metadata for the time-series was last edited.

        :return: When (in UTC) the metadata for the time-series was last edited.
        :rtype: Timestamp
        """
        return self._edited

    @property
    def refreshed(self) -> Timestamp or None:
        """
        Returns when (in UTC) the data in the time-series was last refreshed; can be None if no data has yet been
        entered.

        :return: When (in UTC) the data in the time-series was last refreshed; can be None if no data has yet been
        entered.
        :rtype: Timestamp or None
        """
        return self._refreshed

    @property
    def oldest_date_time(self) -> Timestamp or None:
        """
        Returns the oldest date/time in the associated time-series; can be null if the time-series is empty.

        :return: The oldest date/time in the associated time-series; can be null if the time-series is empty.
        :rtype: Timestamp or None
        """
        return self._oldest_date_time

    @property
    def newest_date_time(self) -> Timestamp or None:
        """
        Returns the newest date/time in the associated time-series; can be null if the time-series is empty.

        :return: The newest date/time in the associated time-series; can be null if the time-series is empty.
        :rtype: Timestamp or None
        """
        return self._newest_date_time

    @staticmethod
    def deserialize(serialized: bytes) -> TimeSeriesMetadata:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: TimeSeriesMetadata
        """
        metadata = TimeSeriesMetadata("a", "a", "a", "", "", "", dict(), Frequency.NONE, dict(), False, Timestamp.now(), Timestamp.now())
        metadata._read_proto(serialized)
        return metadata

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        metadata = TimeSeriesMetadata_pb2.TimeSeriesMetadata()
        metadata.ParseFromString(byte_array)
        self._read_proto_object(metadata)

    def _read_proto_object(self,
                           metadata: TimeSeriesMetadata_pb2.TimeSeriesMetadata):
        """
        Sets the state of this from a provided Protobuf object.

        :param metadata: The Protobuf object.
        :type metadata: TimeSeriesMetadata_pb2.TimeSeriesMetadata
        """
        self._source = metadata.source
        self._code = metadata.code
        self._ts_id = metadata.id
        self._url = metadata.url
        self._summary = metadata.summary
        self._description = metadata.description
        self._features = metadata.features
        self._frequency = Frequency[metadata.frequency]
        self._properties = metadata.properties
        self._premium = metadata.premium

        self._features = dict()
        for key in metadata.features:
            self._features[key] = metadata.features[key]

        self._properties = dict()
        for key in metadata.properties:
            self._properties[key] = metadata.properties[key]

        timestamp = metadata.created
        self._created = get_timestamp(timestamp.epochSecond, timestamp.nanosecond)

        timestamp = metadata.edited
        self._edited = get_timestamp(timestamp.epochSecond, timestamp.nanosecond)

        if metadata.refreshedSet:
            timestamp = metadata.refreshed
            self._refreshed = get_timestamp(timestamp.epochSecond, timestamp.nanosecond)
        else:
            self._refreshed = None

        if metadata.oldestDateTimeSet:
            timestamp = metadata.oldestDateTime
            self._oldest_date_time = get_timestamp(timestamp.epochSecond, timestamp.nanosecond)

            timestamp = metadata.newestDateTime
            self._newest_date_time = get_timestamp(timestamp.epochSecond, timestamp.nanosecond)
        else:
            self._oldest_date_time = None
            self._newest_date_time = None

        self._build_hash_code()

    def _write_proto_object(self) -> TimeSeriesMetadata_pb2.TimeSeriesMetadata:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: TimeSeriesMetadata_pb2.TimeSeriesMetadata
        """
        metadata = TimeSeriesMetadata_pb2.TimeSeriesMetadata()
        metadata.source = self._source
        metadata.code = self._code
        metadata.id = self._ts_id
        metadata.url = self._url
        metadata.summary = self._summary
        metadata.description = self._description
        metadata.frequency = self._frequency.name
        metadata.premium = self._premium

        for key, value in self._features.items():
            metadata.features[key] = value

        for key, value in self._properties.items():
            metadata.properties[key] = value

        timestamp = Timestamp_pb2.Timestamp()
        timestamp.epochSecond = get_secs_from_timestamp(self._created)
        timestamp.nanosecond = get_nanos_from_timestamp(self._created)
        metadata.created.CopyFrom(timestamp)

        timestamp = Timestamp_pb2.Timestamp()
        timestamp.epochSecond = get_secs_from_timestamp(self._edited)
        timestamp.nanosecond = get_nanos_from_timestamp(self._edited)
        metadata.edited.CopyFrom(timestamp)

        if self._refreshed is not None:
            timestamp = Timestamp_pb2.Timestamp()
            timestamp.epochSecond = get_secs_from_timestamp(self._refreshed)
            timestamp.nanosecond = get_nanos_from_timestamp(self._refreshed)
            metadata.refreshed.CopyFrom(timestamp)

            metadata.refreshedSet = True
        else:
            metadata.refreshedSet = False

        if self._oldest_date_time is not None:
            timestamp = Timestamp_pb2.Timestamp()
            timestamp.epochSecond = get_secs_from_timestamp(self._oldest_date_time)
            timestamp.nanosecond = get_nanos_from_timestamp(self._oldest_date_time)
            metadata.oldestDateTime.CopyFrom(timestamp)

            timestamp = Timestamp_pb2.Timestamp()
            timestamp.epochSecond = get_secs_from_timestamp(self._newest_date_time)
            timestamp.nanosecond = get_nanos_from_timestamp(self._newest_date_time)
            metadata.newestDateTime.CopyFrom(timestamp)

            metadata.oldestDateTimeSet = True
        else:
            metadata.oldestDateTimeSet = False

        return metadata

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return: A str containing the state of this serialised.
        :rtype: bytes
        """
        metadata = self._write_proto_object()
        return metadata.SerializeToString()

    def __eq__(self, other):
        if isinstance(other, TimeSeriesMetadata):
            if self._source is None and other._source is not None:
                return False
            elif self._source != other._source:
                return False

            if self._code is None and other._code is not None:
                return False
            elif self._code != other._code:
                return False

            if self._ts_id is None and other._ts_id is not None:
                return False
            elif self._ts_id != other._ts_id:
                return False

            return True

        return False

    def __hash__(self):
        return self._hash_code

    def __str__(self):
        return "Source = " + self._source + \
               "Code = " + self._code + \
               "ID = " + self._ts_id + \
               "URL = " + self._url + \
               "Summary = " + self._summary + \
               "Description = " + self._description + \
               "Frequency = " + self._frequency.name + \
               "Features = " + str(self._features) + \
               "Properties = " + str(self._properties) + \
               "Premium = " + str(self._premium) + \
               "Created = " + get_yyyy_mm_dd_hh_mm_ss_n(self._created) + \
               "Edited = " + get_yyyy_mm_dd_hh_mm_ss_n(self._edited) + \
               "Refreshed = " + get_yyyy_mm_dd_hh_mm_ss_n(self._refreshed) + \
               "Oldest Date/Time = " + get_yyyy_mm_dd_hh_mm_ss_n(self._oldest_date_time) + \
               "Latest Date/Time = " + get_yyyy_mm_dd_hh_mm_ss_n(self._newest_date_time)


class TimeSeriesData:
    """
    Contains the data for a time-series.
    """
    def __init__(self,
                 data: List[Tuple[Timestamp, List[Dict[str, Any]]]]):
        """
        :param data: The data.
        :type data: List[Tuple[datetime, List[Dict[str, Any]]]]
        """
        if not isinstance(data, List):
            raise ValueError("data is not an instance of List")

        # Check the data is of the correct type

        for tuple_item in data:
            # Check that the list item is of the correct type

            if len(tuple_item) != 2:
                raise ValueError("data does not contain tuples all of length 2")

            else:
                # Check that the 1st item is a timestamp

                first_tuple_item = tuple_item[0]

                if not isinstance(first_tuple_item, Timestamp):
                    raise ValueError("data does not contain tuples where the 1st item is a Timestamp")

                # Check that the 2nd item is a List of Dict

                second_tuple_item = tuple_item[1]

                if not isinstance(second_tuple_item, List):
                    raise ValueError("data does not contain tuples where the 2nd item is a List")

                # Check that the items in the feature map are valid

                for feature_map in second_tuple_item:
                    if not isinstance(feature_map, Dict):
                        raise ValueError("data does not contain tuples where the 2nd item is a List containing Dict")

                    for feature_name in feature_map:
                        # Check the feature name

                        if not isinstance(feature_name, str):
                            raise ValueError("data does not contain Dict where all keys are str")

                        if not is_valid_token(feature_name):
                            raise ValueError("data contains a Dict where a key is an invalid token")

                        # Check the feature value

                        feature_value = feature_map[feature_name]

                        if not _valid_feature_value(feature_value):
                            raise ValueError("data does not contain Dict where all the values are valid feature values")

        # Store the sorted data

        self._data = data

    @property
    def data(self) -> List[Tuple[Timestamp, List[Dict[str, object]]]]:
        """
        Returns the data.

        :return: The data.
        :rtype: List[Tuple[Timestamp, List[Dict[str, object]]]]
        """
        return self._data

    @property
    def flattened_data(self) -> List[Tuple[Timestamp, Dict[str, object]]]:
        """
        Used to 'flatten' (one entry per date/time) the data contained within this.

        :return: The "flattened" data.
        :rtype: List[Tuple[Timestamp, Dict[str, object]]]
        """
        flattened = []

        for tuple_item in self._data:
            list_item = tuple_item[1]

            if len(list_item) > 0:
                flattened.append((tuple_item[0], list_item[0]))
            else:
                flattened.append((tuple_item[0], {}))

        return flattened

    @staticmethod
    def _atomic_feature_value_equals(value1: Any,
                                     value2: Any) -> bool:
        """
        Determines if the values of two features containing atomic values are equal.

        :param value1: The 1st feature value.
        :type value1: Any

        :param value2: The 2nd feature value.
        :type value2: Any

        :return: True if the feature values are the same and atomic, False otherwise.
        :rtype: bool
        """
        if value1 is None:
            return value2 is None
        elif isinstance(value1, str) or isinstance(value1, int) or isinstance(value1, float)\
                or isinstance(value1, bool) or isinstance(value1, date) or isinstance(value1, bytes):
            return value1 == value2
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, TimeSeriesData):
            if len(self._data) != len(other._data):
                return False
            else:
                for i, tuple_1 in enumerate(self._data):
                    entry_time_1 = tuple_1[0]
                    tuple_2 = other._data[i]
                    entry_time_2 = tuple_2[0]

                    if entry_time_1 != entry_time_2:
                        return False
                    else:
                        list_1 = tuple_1[1]
                        list_2 = tuple_2[1]

                        if len(list_1) != len(list_2):
                            return False
                        else:
                            for j, map_1 in enumerate(list_1):
                                map_2 = list_2[j]

                                if len(map_1) != len(map_2):
                                    return False
                                else:
                                    for map_1_key in map_1:
                                        if map_1_key not in map_2:
                                            return False
                                        else:
                                            map_1_value = map_1[map_1_key]
                                            map_2_value = map_2[map_1_key]

                                            if not _feature_value_equals(map_1_value, map_2_value):
                                                return False
                return True
        else:
            return False

    @staticmethod
    def deserialize(serialized: bytes) -> TimeSeriesData:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: TimeSeriesData
        """
        time_series_data = TimeSeriesData([])
        time_series_data._read_proto(serialized)
        return time_series_data

    def _read_proto(self,
                    serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        time_series_data = TimeSeriesData_pb2.TimeSeriesData()
        time_series_data.ParseFromString(byte_array)
        self._read_proto_object(time_series_data)

    def _read_proto_object(self,
                           time_series_data: TimeSeriesData_pb2.TimeSeriesData):
        """
        Sets the state of this from a provided Protobuf object.

        :param time_series_data: The Protobuf object.
        :type time_series_data: TimeSeriesData_pb2.TimeSeriesData
        """
        # The below works as the timestamps will be stored in order in the Protobuf object

        last_entry_datetime = None

        for i, timestamp in enumerate(time_series_data.timestamps):
            #  Get object values for the feature map

            proto_feature_map = time_series_data.data[i]
            feature_map = {}

            for feature_name in proto_feature_map.mapValue:
                proto_feature_value = proto_feature_map.mapValue[feature_name]
                feature_map[feature_name] = _get_feature_value_from_proto(proto_feature_value)

            # See how to append the feature map to the data already stored in this

            entry_datetime = get_timestamp(timestamp.epochSecond, timestamp.nanosecond)

            if last_entry_datetime is None or last_entry_datetime != entry_datetime:
                self._data.append((entry_datetime, [feature_map]))
            else:
                self._data[-1][1].append(feature_map)

            # Store that we have encountered another datetime

            last_entry_datetime = entry_datetime

    def _write_proto_object(self) -> TimeSeries_pb2.TimeSeries:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: TimeSeriesMetadataRequest_pb2.TimeSeriesMetadataRequest
        """
        time_series_data = TimeSeriesData_pb2.TimeSeriesData()

        for tuple_item in self._data:
            # Get the Protobuf object for the entry date/time

            entry_time = tuple_item[0]
            timestamp = Timestamp_pb2.Timestamp()
            timestamp.epochSecond = get_secs_from_timestamp(entry_time)
            timestamp.nanosecond = get_nanos_from_timestamp(entry_time)

            # Get the Protobuf objects for the feature maps for this entry date/time

            feature_list = tuple_item[1]

            for feature_map in feature_list:
                # Get a map of Protobuf objects representing the features

                time_series_entry = DataEntry_pb2.DataEntry()
                time_series_entry.isMap = True
                time_series_entry.isList = False
                time_series_entry.isAtomic = False

                for feature_name in feature_map:
                    feature_value = feature_map[feature_name]
                    time_series_entry.mapValue[feature_name].CopyFrom(_get_feature_value(feature_value))

                # Append the features and timestamp to the Protobuf object to return

                time_series_data.timestamps.append(timestamp)
                time_series_data.data.append(time_series_entry)

        return time_series_data

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return: A str containing the state of this serialised.
        :rtype: bytes
        """
        time_series_data = self._write_proto_object()
        return time_series_data.SerializeToString()


class TimeSeries:
    """
    Holds data about a subset of a time-series.
    """
    def __init__(self,
                 metadata: TimeSeriesMetadata,
                 data: TimeSeriesData):
        """
        :param metadata: The metadata.
        :type metadata: TimeSeriesMetadata

        :param data: The data.
        :type data: TimeSeriesData
        """
        # Check the parameters

        if not isinstance(metadata, TimeSeriesMetadata):
            raise ValueError("metadata is not an instance of TimeSeriesMetadata")

        if not isinstance(data, TimeSeriesData):
            raise ValueError("data is not an instance of TimeSeriesData")

        # Store the parameters

        self._metadata = metadata
        self._data = data

    @property
    def metadata(self) -> TimeSeriesMetadata:
        """
        Returns the metadata.

        :return: The metadata.
        :rtype: TimeSeriesMetadata
        """
        return self._metadata

    @property
    def data(self) -> TimeSeriesData:
        """
        Returns the data.

        :return: The data.
        :rtype: TimeSeriesData
        """
        return self._data

    def __eq__(self, other):
        if isinstance(other, TimeSeries):
            if self._metadata is None:
                if other._metadata is not None:
                    return False
            else:
                if self._metadata != other._metadata:
                    return False

            if self._data is None:
                if other._data is not None:
                    return False
            else:
                if self._data != other._data:
                    return False
            return True
        else:
            return False

    @staticmethod
    def deserialize(serialized: bytes) -> TimeSeries:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: TimeSeries
        """
        metadata = TimeSeriesMetadata("a", "a", "a", "", "", "", dict(), Frequency.NONE, dict(), False,
                                      Timestamp.now(), Timestamp.now())
        data = TimeSeriesData([])
        time_series = TimeSeries(metadata, data)
        time_series._read_proto(serialized)
        return time_series

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        time_series = TimeSeries_pb2.TimeSeries()
        time_series.ParseFromString(byte_array)
        self._read_proto_object(time_series)

    def _read_proto_object(self,
                           time_series: TimeSeries_pb2.TimeSeries):
        """
        Sets the state of this from a provided Protobuf object.

        :param time_series: The Protobuf object.
        :type time_series: TimeSeries_pb2.TimeSeries
        """
        self._metadata = TimeSeriesMetadata("a", "a", "a", "", "", "", dict(), Frequency.NONE, dict(), False, Timestamp.now(), Timestamp.now())
        self._metadata._read_proto_object(time_series.metadata)

        self._data = TimeSeriesData([])
        self._data._read_proto_object(time_series.data)

    def _write_proto_object(self) -> TimeSeries_pb2.TimeSeries:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: TimeSeries_pb2.TimeSeries
        """
        time_series = TimeSeries_pb2.TimeSeries()
        time_series.metadata.CopyFrom(self._metadata._write_proto_object())
        time_series.data.CopyFrom(self._data._write_proto_object())

        return time_series

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return: A bytes containing the state of this serialised.
        :rtype: bytes
        """
        time_series = self._write_proto_object()
        return time_series.SerializeToString()


class TimeSeriesMetadataRequest:
    """
    Represents a time-series metadata request.
    """
    def __init__(self,
                 source: str,
                 code: str,
                 ts_id: str,
                 api_key: str = None):
        """
        All parameters should be supplied unless deserializing an object.

        :param source: The source for the time-series.
        :type source: str

        :param code: The code for the time-series.
        :type code: str

        :param ts_id: The ID for the time-series.
        :type ts_id: str

        :param api_key: The API Key.
        :type api_key: str or None
        """
        # Check if the data is valid

        if api_key is not None and not isinstance(api_key, str):
            raise ValueError("api_key is not None or a valid str")

        if api_key is not None and not is_valid_token(api_key):
            raise ValueError("api_key is not valid")

        if not isinstance(source, str):
            raise ValueError("source is not a valid str")

        if not is_valid_token(source):
            raise ValueError("source is not valid")

        if not isinstance(code, str):
            raise ValueError("code is not a valid str")

        if not is_valid_token(code):
            raise ValueError("code is not valid")

        if not isinstance(ts_id, str):
            raise ValueError("ts_id is not a valid str")

        if not is_valid_token(ts_id):
            raise ValueError("ts_id is not valid")

        # Store the data

        self._api_key = api_key
        self._source = source
        self._code = code
        self._ts_id = ts_id
        self._client_type = ClientType.PYTHON_CLIENT

    @property
    def api_key(self) -> str:
        """
        Returns the API Key.

        :return: The API Key.
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        """
        Sets the new value for the API Key.

        :param value: The new value for the API Key.
        :type value: str
        """
        if value is not None and not isinstance(value, str):
            raise ValueError("value is not None or a valid str")

        if value is not None and not is_valid_token(value):
            raise ValueError("value is not valid")

        self._api_key = value

    @property
    def source(self) -> str:
        """
        Returns the source for the time-series.

        :return: The source for the time-series.
        :rtype: str
        """
        return self._source

    @property
    def code(self) -> str:
        """
        Returns the code for the time-series.

        :return: The code for the time-series.
        :rtype: str
        """
        return self._code

    @property
    def ts_id(self) -> str:
        """
        Returns the ID for the time-series.

        :return: The ID for the time-series.
        :rtype: str
        """
        return self._ts_id

    @property
    def client_type(self) -> str:
        """
        Returns the type of client that sent this request.

        :return: The type of client that sent this request.
        :rtype: str
        """
        return self._client_type

    @staticmethod
    def deserialize(serialized: bytes) -> TimeSeriesMetadataRequest:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: TimeSeriesMetadataRequest
        """
        request = TimeSeriesMetadataRequest("a", "a", "a", "a")
        request._read_proto(serialized)
        return request

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        request = TimeSeriesMetadataRequest_pb2.TimeSeriesMetadataRequest()
        request.ParseFromString(byte_array)
        self._read_proto_object(request)

    def _read_proto_object(self, metadata_request: TimeSeriesMetadataRequest_pb2.TimeSeriesMetadataRequest):
        """
        Sets the state of this from a provided Protobuf object.

        :param metadata_request: The Protobuf object.
        :type metadata_request: TimeSeriesMetadataRequest_pb2.TimeSeriesMetadataRequest
        """
        self._api_key = metadata_request.apiKey
        self._source = metadata_request.source
        self._code = metadata_request.code
        self._ts_id = metadata_request.id
        self._client_type = metadata_request.clientType

    def _write_proto_object(self) -> TimeSeriesMetadataRequest_pb2.TimeSeriesMetadataRequest:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: TimeSeriesMetadataRequest_pb2.TimeSeriesMetadataRequest
        """
        request = TimeSeriesMetadataRequest_pb2.TimeSeriesMetadataRequest()
        request.apiKey = self._api_key
        request.source = self._source
        request.code = self._code
        request.id = self._ts_id
        request.clientType = self._client_type

        return request

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return: A bytes containing the state of this serialised.
        :rtype: bytes
        """
        request = self._write_proto_object()
        return request.SerializeToString()


class TimeSeriesMetadataResponse:
    """
    Represents the response to a time-series metadata request.
    """
    def __init__(self,
                 metadata: TimeSeriesMetadata = None,
                 error_code: int = None,
                 error_message: str = None):
        """
        Either error_code and error_message should be supplied (with metadata None), or just metadata.

        :param metadata: The data to return.
        :type metadata: TimeSeriesMetadata

        :param error_code: The error code.
        :type error_code: int

        :param error_message: The error message.
        :type error_message: str
        """
        if error_code is None:
            if not isinstance(metadata, TimeSeriesMetadata):
                raise ValueError("metadata is not an instance of TimeSeriesMetadata")

            if error_message is not None:
                raise ValueError("error_code is None and error_message is not None")

            self._error_occurred = False
            self._error_code = 0
            self._error_message = None
            self._metadata = metadata

        else:
            if not isinstance(error_code, int):
                raise ValueError("error_code is not None and is not a valid int")

            if not isinstance(error_message, str):
                raise ValueError("error_code is not None and error_message is not a valid str")

            if metadata is not None:
                raise ValueError("error_code is not None and metadata is not None")

            self._error_occurred = True
            self._error_code = error_code
            self._error_message = error_message
            self._metadata = None

    @property
    def error_occurred(self) -> bool:
        """
        Returns True if an error has occurred, False otherwise.

        :return: True if an error has occurred, False otherwise.
        :rtype: bool
        """
        return self._error_occurred

    @property
    def error_code(self) -> int:
        """
        Returns the error code if an error occurred, 0 otherwise.

        :return: The error code if an error occurred, 0 otherwise.
        :rtype: int
        """
        return self._error_code

    @property
    def error_message(self) -> str:
        """
        Returns the error message if an error occurred, None otherwise.

        :return: The error message if an error occurred, None otherwise.
        :rtype: str
        """
        return self._error_message

    @property
    def metadata(self) -> TimeSeriesMetadata:
        """
        Returns the data to return if an error did not occur, None otherwise.

        :return: The data to return if an error did not occur, None otherwise.
        :rtype: TimeSeriesMetadata
        """
        return self._metadata

    @staticmethod
    def deserialize(serialized: bytes) -> TimeSeriesMetadataResponse:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: TimeSeriesMetadataResponse
        """
        response = TimeSeriesMetadataResponse(error_code=0, error_message="")
        response._read_proto(serialized)
        return response

    def _read_proto(self,
                    serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        response = TimeSeriesMetadataResponse_pb2.TimeSeriesMetadataResponse()
        response.ParseFromString(byte_array)
        self._read_proto_object(response)

    def _read_proto_object(self,
                           response: TimeSeriesMetadataResponse_pb2.TimeSeriesMetadataResponse):
        """
        Sets the state of this from a provided Protobuf object.

        :param response: The Protobuf object.
        :type response: TimeSeriesMetadataResponse_pb2.TimeSeriesMetadataResponse
        """
        self._error_occurred = response.errorHasOccurred

        if self._error_occurred:
            self._error_code = response.errorCode
            self._error_message = response.errorMessage
            self._metadata = None
        else:
            self._error_code = 0
            self._error_message = None
            self._metadata = TimeSeriesMetadata("a", "a", "a", "", "", "", dict(), Frequency.NONE, dict(), False,Timestamp.now(), Timestamp.now())
            self._metadata._read_proto_object(response.metadata)

    def _write_proto_object(self) -> TimeSeriesMetadataResponse_pb2.TimeSeriesMetadataResponse:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: TimeSeriesMetadataRequest_pb2.TimeSeriesMetadataRequest
        """
        response = TimeSeriesMetadataResponse_pb2.TimeSeriesMetadataResponse()
        response.errorHasOccurred = self._error_occurred

        if self._error_occurred:
            response.errorCode = self._error_code
            response.errorMessage = self._error_message
        else:
            response.metadata.CopyFrom(self._metadata._write_proto_object())

        return response

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return: A bytes containing the state of this serialised.
        :rtype: bytes
        """
        response = self._write_proto_object()
        return response.SerializeToString()


class TimeSeriesRequest:
    """
    Represents a time-series request.
    """
    def __init__(self,
                 source: str,
                 code: str,
                 ts_id: str,
                 start: Timestamp = None,
                 end: Timestamp = None,
                 features: List[str] = None,
                 max_size: int = -1,
                 ascending: bool = True,
                 filters: Dict[str, str] = None,
                 api_key: str = None):
        """
        :param source: The source for the time-series.
        :type source: str

        :param code: The code for the time-series.
        :type code: str

        :param ts_id: The ID for the time-series.
        :type ts_id: str

        :param start: The (optional) start date/time, or None.
        :type start: Timestamp

        :param end: The (optional) end date/time, or None.
        :type end: Timestamp

        :param features: The (optional) list of features, or None.
        :type features: List[str]

        :param max_size: The (optional) maximum number of items that can be returned, or -1 if there should be no limit.
        :type max_size: int

        :param ascending: True if the data should be returned in ascending order, False otherwise.
        :type ascending: bool

        :param filters: The filters that should be applied.
        :type filters: Dict[str, str]

        :param api_key: The (optional) API Key.
        :type api_key: str
        """
        # Check if the data is valid

        if api_key is not None and not isinstance(api_key, str):
            raise ValueError("api_key is not None or a valid str")

        if api_key is not None and not is_valid_token(api_key):
            raise ValueError("api_key is not valid")

        if not isinstance(source, str):
            raise ValueError("source is not a valid str")

        if not is_valid_token(source):
            raise ValueError("source is not valid")

        if not isinstance(code, str):
            raise ValueError("code is not a valid str")

        if not is_valid_token(code):
            raise ValueError("code is not valid")

        if not isinstance(ts_id, str):
            raise ValueError("ts_id is not a valid str")

        if not is_valid_token(ts_id):
            raise ValueError("ts_id is not valid")

        if start is not None:
            if not isinstance(start, Timestamp):
                raise ValueError("start is not a Timestamp")

        if end is not None:
            if not isinstance(end, Timestamp):
                raise ValueError("end is not a Timestamp")

        if features is not None:
            if not isinstance(features, list):
                raise ValueError("features is not a list")

            for item in features:
                if not isinstance(item, str):
                    raise ValueError("features does not contain only instances of str ")
                elif not is_valid_token(item):
                    raise ValueError("\"{}\" is not a valid name for a feature".format(item))

        if not isinstance(max_size, int):
            raise ValueError("maxSize is not an int")

        if max_size < -1:
            raise ValueError("maxSize is less than -1")

        if not isinstance(ascending, bool):
            raise ValueError("ascending is not an bool")

        if filters is None:
            filters = {}

        if not isinstance(filters, dict):
            raise ValueError("filters is not a dict")

        for feature_name in filters.keys():
            if not isinstance(feature_name, str):
                raise ValueError("filters does not contain only instances of str ")
            
            feature_filter = filters[feature_name]
            if not isinstance(feature_filter, str):
                raise ValueError("filters does not contain only instances of str ")

        # Store the data

        self._api_key = api_key
        self._source = source
        self._code = code
        self._ts_id = ts_id
        self._start = start
        self._end = end
        self._features = features
        self._max_size = max_size
        self._ascending = ascending
        self._filters = filters
        self._client_type = ClientType.PYTHON_CLIENT

    @property
    def api_key(self) -> str or None:
        """
        Returns the API Key.

        :return: The API Key.
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        """
        Sets the new value for the API Key.

        :param value: The new value for the API Key.
        :type value: str
        """
        if value is not None and not isinstance(value, str):
            raise ValueError("value is not None or a valid str")

        self._api_key = value

    @property
    def source(self) -> str:
        """
        Returns the source for the time-series.

        :return: The source for the time-series.
        :rtype: str
        """
        return self._source

    @property
    def code(self) -> str:
        """
        Returns the code for the time-series.

        :return: The code for the time-series.
        :rtype: str
        """
        return self._code

    @property
    def ts_id(self) -> str:
        """
        Returns the ID for the time-series.

        :return: The ID for the time-series.
        :rtype: str
        """
        return self._ts_id

    @property
    def start(self) -> Timestamp or None:
        """
        Returns the (optional) start date/time, or None.

        :return: The (optional) start date/time, or None.
        :rtype: Timestamp or None
        """
        return self._start

    @property
    def end(self) -> Timestamp or None:
        """
        Returns the (optional) end date/time, or None.

        :return: The (optional) end date/time, or None.
        :rtype: Timestamp
        """
        return self._end

    @property
    def features(self) -> List[str] or None:
        """
        Returns the (optional) list of features, or None.

        :return: The (optional) list of features, or None.
        :rtype: List[str]
        """
        return self._features

    @property
    def max_size(self) -> int:
        """
        Returns the maximum number of items that can be returned, or -1 if there should be no limit.

        :return: The maximum number of items that can be returned, or -1 if there should be no limit.
        :rtype: int
        """
        return self._max_size

    @property
    def ascending(self) -> bool:
        """
        Returns True if the data should be returned in ascending order, False otherwise.

        :return: True if the data should be returned in ascending order, False otherwise.
        :rtype: bool
        """
        return self._ascending

    @property
    def filters(self) -> Dict[str, str]:
        """
        Returns the filters that should be applied.

        :return: The filters that should be applied.
        :rtype: Dict[str, str]
        """
        return self._filters

    @property
    def client_type(self) -> str:
        """
        Returns the type of client that sent this request.

        :return: The type of client that sent this request.
        :rtype: str
        """
        return self._client_type

    @staticmethod
    def deserialize(serialized: bytes) -> TimeSeriesRequest:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: TimeSeriesRequest
        """
        request = TimeSeriesRequest("a", "a", "a", Timestamp.now(), Timestamp.now(), ["Example"], -1, True, {}, "a")
        request._read_proto(serialized)
        return request

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        request = TimeSeriesRequest_pb2.TimeSeriesRequest()
        request.ParseFromString(byte_array)
        self._read_proto_object(request)

    @staticmethod
    def _get_datetime(timestamp: Timestamp_pb2.Timestamp) -> Timestamp or None:
        """
        Return the Timestamp for timestamp, or None if timestamp is None.
 d
        :param timestamp: Timestamp_pb2.Timestamp
        :type timestamp: The Protobuf timestamp (which may be None).

        :return: The datetime for timestamp, or None if timestamp is None.
        :rtype: Timestamp or None
        """
        if timestamp is None:
            return None
        else:
            return get_timestamp(timestamp.epochSecond, timestamp.nanosecond)

    def _read_proto_object(self,
                           request: TimeSeriesRequest_pb2.TimeSeriesRequest):
        """
        Sets the state of this from a provided Protobuf object.

        :param request: The Protobuf object.
        :type request: TimeSeriesRequest_pb2.TimeSeriesRequest
        """
        self._api_key = request.apiKey
        self._source = request.source
        self._code = request.code
        self._ts_id = request.id

        if request.startSet:
            self._start = TimeSeriesRequest._get_datetime(request.start)
        else:
            self._start = None

        if request.endSet:
            self._end = TimeSeriesRequest._get_datetime(request.end)
        else:
            self._end = None

        if request.featuresSet:
            self._features = request.features
        else:
            self._features = None

        self._max_size = request.maxSize
        self._ascending = request.ascending

        self._filters = {}

        if request.filters:
            for key in request.filters:
                value = request.filters[key]
                self._filters[key] = value

        self._client_type = request.clientType

    def _write_proto_object(self) -> TimeSeriesRequest_pb2.TimeSeriesRequest:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: TimeSeriesRequest_pb2.TimeSeriesRequest
        """
        request = TimeSeriesRequest_pb2.TimeSeriesRequest()
        request.apiKey = self._api_key
        request.source = self._source
        request.code = self._code
        request.id = self.ts_id

        if self._start is None:
            request.startSet = False
        else:
            request.startSet = True
            timestamp = Timestamp_pb2.Timestamp()
            timestamp.epochSecond = get_secs_from_timestamp(self._start)
            timestamp.nanosecond = get_nanos_from_timestamp(self._start)
            request.start.CopyFrom(timestamp)

        if self._end is None:
            request.endSet = False
        else:
            request.endSet = True
            timestamp = Timestamp_pb2.Timestamp()
            timestamp.epochSecond = get_secs_from_timestamp(self._end)
            timestamp.nanosecond = get_nanos_from_timestamp(self._end)
            request.end.CopyFrom(timestamp)

        if self._features is not None:
            request.featuresSet = True

            for item in self.features:
                request.features.append(item)
        else:
            request.featuresSet = False

        request.maxSize = self._max_size
        request.ascending = self._ascending
        request.filters.update(self._filters)
        request.clientType = self._client_type

        return request

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return: A bytes containing the state of this serialised.
        :rtype: bytes
        """
        request = self._write_proto_object()
        return request.SerializeToString()


class TimeSeriesResponse:
    """
    Represents the response to a time-series request.
    """
    def __init__(self,
                 data: TimeSeries = None,
                 error_code: int = None,
                 error_message: str = None):
        """
        Either error_code and error_message should be supplied (with data None), or just data.

        :param data: The data to return.
        :type data: TimeSeries

        :param error_code: The error code.
        :type error_code: int

        :param error_message: The error message.
        :type error_message: str
        """
        if error_code is None:
            if not isinstance(data, TimeSeries):
                raise ValueError("data is not an instance of TimeSeries")

            if error_message is not None:
                raise ValueError("error_code is None and error_message is not None")

            self._error_occurred = False
            self._error_code = 0
            self._error_message = None
            self._data = data

        else:
            if not isinstance(error_code, int):
                raise ValueError("error_code is not None and is not a valid int")

            if not isinstance(error_message, str):
                raise ValueError("error_code is not None and error_message is not a valid str")

            if data is not None:
                raise ValueError("error_code is not None and data is not None")

            self._error_occurred = True
            self._error_code = error_code
            self._error_message = error_message
            self._data = None

    @property
    def error_occurred(self) -> bool:
        """
        Returns True if an error has occurred, False otherwise.

        :return: True if an error has occurred, False otherwise.
        :rtype: bool
        """
        return self._error_occurred

    @property
    def error_code(self) -> int:
        """
        Returns the error code if an error occurred, 0 otherwise.

        :return: The error code if an error occurred, 0 otherwise.
        :rtype: int
        """
        return self._error_code

    @property
    def error_message(self) -> str:
        """
        Returns the error message if an error occurred, None otherwise.

        :return: The error message if an error occurred, None otherwise.
        :rtype: str
        """
        return self._error_message

    @property
    def data(self) -> TimeSeries:
        """
        Returns the data to return if an error did not occur, None otherwise.

        :return: The data to return if an error did not occur, None otherwise.
        :rtype: TimeSeries
        """
        return self._data

    @staticmethod
    def deserialize(serialized: bytes) -> TimeSeriesResponse:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: TimeSeriesResponse
        """
        response = TimeSeriesResponse(error_code=0, error_message="")
        response._read_proto(serialized)
        return response

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        response = TimeSeriesResponse_pb2.TimeSeriesResponse()
        response.ParseFromString(byte_array)
        self._read_proto_object(response)

    def _read_proto_object(self,
                           response: TimeSeriesResponse_pb2.TimeSeriesResponse):
        """
        Sets the state of this from a provided Protobuf object.

        :param response: The Protobuf object.
        :type response: TimeSeriesResponse_pb2.TimeSeriesResponse
        """
        self._error_occurred = response.errorHasOccurred

        if self._error_occurred:
            self._error_code = response.errorCode
            self._error_message = response.errorMessage
            self._data = None
        else:
            self._error_code = 0
            self._error_message = None
            self._data = TimeSeries(TimeSeriesMetadata("a", "a", "a", "", "", "", dict(), Frequency.NONE, dict(), False, Timestamp.now(), Timestamp.now()), TimeSeriesData([]))
            self._data._read_proto_object(response.timeSeries)

    def _write_proto_object(self) -> TimeSeriesResponse_pb2.TimeSeriesResponse:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: TimeSeriesResponse_pb2.TimeSeriesResponse
        """
        response = TimeSeriesResponse_pb2.TimeSeriesResponse()
        response.errorHasOccurred = self._error_occurred

        if self._error_occurred:
            response.errorCode = self._error_code
            response.errorMessage = self._error_message
        else:
            response.timeSeries.CopyFrom(self._data._write_proto_object())

        return response

    def serialize(self) -> bytes:
        """
        Returns a str containing the state of this serialised.

        :return: A str containing the state of this serialised.
        :rtype: bytes
        """
        response = self._write_proto_object()
        return response.SerializeToString()
