"""
Classes and functions related to collections.
"""
from __future__ import annotations

from archipelagos.common.data import get_secs_from_timestamp, get_nanos_from_timestamp, get_timestamp
from archipelagos.common.data import get_yyyy_mm_dd_hh_mm_ss_n
from archipelagos.common.protobuf.common.data.collection import CollectionMetadata_pb2, CollectionData_pb2
from archipelagos.common.protobuf.common.data.collection import Collection_pb2
from archipelagos.common.protobuf.common.data.collection import CollectionRequest_pb2, CollectionResponse_pb2
from archipelagos.common.protobuf.common.data.collection import CollectionMetadataResponse_pb2
from archipelagos.common.protobuf.common.data.collection import CollectionMetadataRequest_pb2
from archipelagos.common.protobuf.common.data import DataEntry_pb2
from archipelagos.common.protobuf.common import Timestamp_pb2
from archipelagos.common.data import _valid_feature_value, _feature_value_equals
from archipelagos.common.data import _get_feature_value, _get_feature_value_from_proto
from archipelagos.common.platform import ClientType

from archipelagos.common.data import Frequency, is_valid_token

import array
from typing import Dict, List
from datetime import datetime
from pandas import Timestamp


class CollectionMetadata:
    """Represents the metadata about a collection.
    """
    def __init__(self,
                 source: str,
                 code: str,
                 cid: str,
                 url: str,
                 summary: str,
                 description: str,
                 features: Dict[str, str],
                 properties: Dict[str, str],
                 premium: bool,
                 created: Timestamp,
                 edited: Timestamp,
                 refreshed: Timestamp = None):
        """
        All parameters should be supplied unless deserializing an object.

        :param source: The source for the collection.
        :type source: str

        :param code: The code for the collection.
        :type code: str

        :param cid: The ID for the collection.
        :type cid: str

        :param url: The URL for the collection..
        :type url: str

        :param summary: The summary for the collection.
        :type summary: str

        :param description: The description for the collection.
        :type description: str

        :param features: The collection's features and their descriptions.
        :type features: Dict[str, str]

        :param properties: The collection's properties.
        :type properties: Dict[str, str]

        :param premium: True if the collection is premium, False otherwise.
        :type premium: bool

        :param created: When (in UTC) the collection was created.
        :type created: Timestamp

        :param edited: When (in UTC) the metadata for the collection was last edited.
        :type edited: Timestamp

        :param refreshed: When (in UTC) the data in the collection was last refreshed; can be None if no data has yet been entered.
        :type refreshed: Timestamp
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

        if not isinstance(cid, str):
            raise ValueError("cid is not a valid str")

        if not is_valid_token(code):
            raise ValueError("cid is not valid")

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

        if not isinstance(premium, bool):
            raise ValueError("premium is not a valid bool")

        if not isinstance(created, Timestamp):
            raise ValueError("created is not a valid Timestamp")

        if not isinstance(edited, Timestamp):
            raise ValueError("edited is not a valid Timestamp")

        if edited < created:
            raise ValueError("edited is before created")

        if refreshed is not None and refreshed < created:
            raise ValueError("refreshed is before created")

        # Store the data

        self._source = source
        self._code = code
        self._cid = cid
        self._url = url
        self._summary = summary
        self._description = description
        self._features = features
        self._properties = properties
        self._premium = premium
        self._created = created
        self._edited = edited
        self._refreshed = refreshed

        self._build_hash_code()

    def _build_hash_code(self):
        """
        Calculates and caches the hash code associated with this.
        """

        prime = 31
        result = 1

        result = prime * result + hash(self._source) if self._source is not None else 0
        result = prime * result + hash(self._code) if self._code is not None else 0
        result = prime * result + hash(self._cid) if self._cid is not None else 0

        self._hash_code = result

    @property
    def source(self) -> str:
        """
        Returns the source for the collection.

        :return: The source for the collection.
        :rtype: str
        """
        return self._source

    @property
    def code(self) -> str:
        """
        Returns the code for the collection.

        :return: The code for the collection.
        :rtype: str
        """
        return self._code

    @property
    def cid(self) -> str:
        """
        Returns the ID for the collection.

        :return: The ID for the collection.
        :rtype: str
        """
        return self._cid

    @property
    def url(self) -> str:
        """
        Returns the url for the collection.

        :return: The url for the collection.
        :rtype: str
        """
        return self._url

    @property
    def summary(self) -> str:
        """
        Returns the summary for the collection.

        :return: The summary for the collection.
        :rtype: str
        """
        return self._summary

    @property
    def description(self) -> str:
        """
        Returns the description for the collection.

        :return: The description for the collection.
        :rtype: str
        """
        return self._description

    @property
    def features(self) -> dict:
        """
        Returns the time-collection's features and their descriptions.

        :return: The time-collection's features and their descriptions.
        :rtype: Frequency
        """
        return self._features

    @property
    def properties(self) -> dict:
        """
        Returns the collection's properties.

        :return: The collection's properties.
        :rtype: Frequency
        """
        return self._properties

    @property
    def premium(self) -> bool:
        """
        Returns True if the collection is premium, False otherwise.

        :return: True if the collection is premium, False otherwise.
        :rtype: bool
        """
        return self._premium

    @property
    def created(self) -> Timestamp:
        """
        Returns when (in UTC) the collection was created.

        :return: When (in UTC) the collection was created.
        :rtype: Timestamp
        """
        return self._created

    @property
    def edited(self) -> Timestamp:
        """
        Returns when (in UTC) the metadata for the collection was last edited.

        :return: When (in UTC) the metadata for the collection was last edited.
        :rtype: datetime
        """
        return self._edited

    @property
    def refreshed(self) -> Timestamp or None:
        """
        Returns when (in UTC) the data in the collection was last refreshed; can be None if no data has been entered.

        :return: When (in UTC) the data in the collection was last refreshed; can be None if no data has been entered.
        :rtype: datetime or None
        """
        return self._refreshed

    @staticmethod
    def deserialize(serialized: bytes) -> CollectionMetadata:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: Creates a new instance using a str created by serialize().
        :rtype: CollectionMetadata
        """
        metadata = CollectionMetadata("a", "a", "a", "", "", "", dict(), dict(), False, Timestamp.now(), Timestamp.now())
        metadata._read_proto(serialized)
        return metadata

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        metadata = CollectionMetadata_pb2.CollectionMetadata()
        metadata.ParseFromString(byte_array)
        self._read_proto_object(metadata)

    def _read_proto_object(self, metadata: CollectionMetadata_pb2.CollectionMetadata):
        """
        Sets the state of this from a provided Protobuf object.

        :param metadata: The Protobuf object.
        :type metadata: CollectionMetadata_pb2.CollectionMetadata
        """
        self._source = metadata.source
        self._code = metadata.code
        self._cid = metadata.id
        self._url = metadata.url
        self._summary = metadata.summary
        self._description = metadata.description
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

        self._build_hash_code()

    def _write_proto_object(self) -> CollectionMetadata_pb2.CollectionMetadata:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: CollectionMetadata_pb2.CollectionMetadata
        """
        metadata = CollectionMetadata_pb2.CollectionMetadata()
        metadata.source = self._source
        metadata.code = self._code
        metadata.id = self._cid
        metadata.url = self._url
        metadata.summary = self._summary
        metadata.description = self._description
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

        return metadata

    def serialize(self) -> bytes:
        """
        Serializes the state of this as a str.

        :return: A bytes containing the state of this serialised.
        :rtype: bytes
        """
        metadata = self._write_proto_object()
        return metadata.SerializeToString()

    def __eq__(self, other):
        if isinstance(other, CollectionMetadata):
            if self._source is None and other._source is not None:
                return False
            elif self._source != other._source:
                return False

            if self._code is None and other._code is not None:
                return False
            elif self._code != other._code:
                return False

            if self._cid is None and other._cid is not None:
                return False
            elif self._cid != other._cid:
                return False

            return True

        return False

    def __hash__(self):
        return self._hash_code

    def __str__(self):
        return "Source = " + self._source + \
               "Code = " + self._code + \
               "ID = " + self._cid + \
               "URL = " + self._url + \
               "Summary = " + self._summary + \
               "Description = " + self._description + \
               "Features = " + str(self._features) + \
               "Properties = " + str(self._properties) + \
               "Premium = " + str(self._premium) + \
               "Created = " + get_yyyy_mm_dd_hh_mm_ss_n(self._created) + \
               "Edited = " + get_yyyy_mm_dd_hh_mm_ss_n(self._edited) + \
               "Refreshed = " + get_yyyy_mm_dd_hh_mm_ss_n(self._refreshed)


class CollectionData:
    """
    Contains the data for a collection.
    """
    def __init__(self, data: Dict[str, Dict[str, object]]):
        """
        :param data: The data.
        :type data: Dict[str, Dict[str, object]]
        """
        if not isinstance(data, Dict):
            raise ValueError("data is not an instance of Dict")

        # Check the data is of the correct type

        for object_id in data:
            # Check that the ID is a str

            if not isinstance(object_id, str):
                raise ValueError("data does not contain keys which are all of type str")

            # Check that the value is a Dict

            feature_map = data[object_id]

            if not isinstance(feature_map, Dict):
                raise ValueError("The value for ID \"{}\" is not a Dict".format(object_id))

            # Check that the items in the feature map are valid

            for feature_name in feature_map:
                # Check the feature name

                if not isinstance(feature_name, str):
                    raise ValueError(
                        "The value for ID \"{}\" contains a Dict where the key is not a str".format(object_id))

                if not is_valid_token(feature_name):
                    raise ValueError(
                        "The value for ID \"{}\" contains a key \"{}\" which is not a valid token".format(
                            object_id, feature_name))

                # Check the feature value

                feature_value = feature_map[feature_name]

                if not _valid_feature_value(feature_value):
                    raise ValueError(
                        "The value for ID \"{}\" contains a key \"{}\" where the associated value is invalid".format(
                            object_id, feature_name))

        # Store the sorted data

        self._data = data

    @property
    def data(self) -> Dict[str, Dict[str, object]]:
        """
        Returns the data.

        :return: The data.
        :rtype: Dict[str, Dict[str, object]]
        """
        return self._data

    @property
    def flattened_data(self) -> List[Dict[str, object]]:
        """
        Used to 'flatten' (one entry per date/time) the data contained within this.

        :return: The "flattened" data.
        :rtype: List[Dict[str, object]]
        """
        return list(self._data.values())

    def __eq__(self, other):
        if isinstance(other, CollectionData):
            if len(self._data) != len(other._data):
                return False
            else:
                for object_id in self._data:
                    if object_id not in other._data:
                        return False
                    else:
                        feature_map_1 = self._data[object_id]
                        feature_map_2 = other._data[object_id]

                        if len(feature_map_1) != len(feature_map_2):
                            return False
                        else:
                            for feature_name in feature_map_1:
                                if feature_name not in feature_map_2:
                                    return False
                                else:
                                    map_1_value = feature_map_1[feature_name]
                                    map_2_value = feature_map_2[feature_name]

                                    if not _feature_value_equals(map_1_value, map_2_value):
                                        return False
                return True
        else:
            return False

    @staticmethod
    def deserialize(serialized: bytes) -> CollectionData:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: CollectionData
        """
        collection_data = CollectionData({})
        collection_data._read_proto(serialized)
        return collection_data

    def _read_proto(self,
                    serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        collection_data = CollectionData_pb2.CollectionData()
        collection_data.ParseFromString(byte_array)
        self._read_proto_object(collection_data)

    def _read_proto_object(self,
                           collection_data: CollectionData_pb2.CollectionData):
        """
        Sets the state of this from a provided Protobuf object.

        :param collection_data: The Protobuf object.
        :type collection_data: CollectionData_pb2.CollectionData
        """
        for i, object_id in enumerate(collection_data.ids):
            #  Get object values for the feature map

            proto_feature_map = collection_data.data[i]
            feature_map = {}

            for feature_name in proto_feature_map.mapValue:
                proto_feature_value = proto_feature_map.mapValue[feature_name]
                feature_map[feature_name] = _get_feature_value_from_proto(proto_feature_value)

            self._data[object_id] = feature_map

    def _write_proto_object(self) -> Collection_pb2.Collection:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: CollectionMetadataRequest_pb2.CollectionMetadataRequest
        """
        collection_data = CollectionData_pb2.CollectionData()

        for object_id in self._data:
            # Get a map of Protobuf objects representing the features

            feature_map = self._data[object_id]
            data_entry = DataEntry_pb2.DataEntry()
            data_entry.isMap = True
            data_entry.isList = False
            data_entry.isAtomic = False

            for feature_name in feature_map:
                feature_value = feature_map[feature_name]
                data_entry.mapValue[feature_name].CopyFrom(_get_feature_value(feature_value))

            # Append the features and timestamp to the Protobuf object to return

            collection_data.ids.append(object_id)
            collection_data.data.append(data_entry)

        return collection_data

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return: A bytes containing the state of this serialised.
        :rtype: bytes
        """
        collection_data = self._write_proto_object()
        return collection_data.SerializeToString()


class Collection:
    """
    Holds data about a subset of a collection.
    """
    def __init__(self,
                 metadata: CollectionMetadata,
                 data: CollectionData):
        """
        :param metadata: The metadata.
        :type metadata: CollectionMetadata

        :param data: The data.
        :type data: CollectionData
        """
        # Check the parameters

        if not isinstance(metadata, CollectionMetadata):
            raise ValueError("metadata is not an instance of CollectionMetadata")

        if not isinstance(data, CollectionData):
            raise ValueError("data is not an instance of CollectionData")

        # Store the parameters

        self._metadata = metadata
        self._data = data

    @property
    def metadata(self) -> CollectionMetadata:
        """
        Returns the metadata.

        :return: The metadata.
        :rtype: CollectionMetadata
        """
        return self._metadata

    @property
    def data(self) -> CollectionData:
        """
        Returns the data.

        :return: The data.
        :rtype: CollectionData
        """
        return self._data

    def __eq__(self, other):
        if isinstance(other, Collection):
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
    def deserialize(serialized: bytes) -> Collection:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: Collection
        """
        metadata = CollectionMetadata("a", "a", "a", "", "", "", dict(), dict(), False, Timestamp.now(), Timestamp.now())
        data = CollectionData({})
        collection = Collection(metadata, data)
        collection._read_proto(serialized)
        return collection

    def _read_proto(self,
                    serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        collection = Collection_pb2.Collection()
        collection.ParseFromString(byte_array)
        self._read_proto_object(collection)

    def _read_proto_object(self,
                           collection: Collection_pb2.Collection):
        """
        Sets the state of this from a provided Protobuf object.

        :param collection: The Protobuf object.
        :type collection: Collection_pb2.Collection
        """
        self._metadata = CollectionMetadata("a", "a", "a", "", "", "", dict(), dict(), False, Timestamp.now(), Timestamp.now())
        self._metadata._read_proto_object(collection.metadata)

        self._data = CollectionData({})
        self._data._read_proto_object(collection.data)

    def _write_proto_object(self) -> Collection_pb2.Collection:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: Collection_pb2.Collection
        """
        collection = Collection_pb2.Collection()
        collection.metadata.CopyFrom(self._metadata._write_proto_object())
        collection.data.CopyFrom(self._data._write_proto_object())

        return collection

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return:  bytes containing the state of this serialised.
        :rtype: bytes
        """
        collection = self._write_proto_object()
        return collection.SerializeToString()


class CollectionMetadataRequest:
    """
    Represents a collection metadata request.
    """
    def __init__(self,
                 source: str,
                 code: str,
                 cid: str,
                 api_key: str = None):
        """
        All parameters should be supplied unless deserializing an object.

        :param source: The source for the collection.
        :type :source str

        :param code: The code for the collection.
        :type code: str

        :param cid: The ID for the collection.
        :type cid: str

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

        if not isinstance(cid, str):
            raise ValueError("cid is not a valid str")

        if not is_valid_token(cid):
            raise ValueError("cid is not valid")

        # Store the data

        self._api_key = api_key
        self._source = source
        self._code = code
        self._cid = cid
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
    def api_key(self,
                value: str):
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
        Returns the source for the collection.

        :return: The source for the collection.
        :rtype: str
        """
        return self._source

    @property
    def code(self) -> str:
        """
        Returns the code for the collection.

        :return: The code for the collection.
        :rtype: str
        """
        return self._code

    @property
    def cid(self) -> str:
        """
        Returns the ID for the collection.

        :return: The ID for the collection.
        :rtype: str
        """
        return self._cid

    @property
    def client_type(self) -> str:
        """
        Returns the type of client that sent this request.

        :return: The type of client that sent this request.
        :rtype: str
        """
        return self._client_type

    @staticmethod
    def deserialize(serialized: bytes) -> CollectionMetadataRequest:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: CollectionMetadataRequest
        """
        request = CollectionMetadataRequest("a", "a", "a", "a")
        request._read_proto(serialized)
        return request

    def _read_proto(self,
                    serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        request = CollectionMetadataRequest_pb2.CollectionMetadataRequest()
        request.ParseFromString(byte_array)
        self._read_proto_object(request)

    def _read_proto_object(self,
                           metadata_request: CollectionMetadataRequest_pb2.CollectionMetadataRequest):
        """
        Sets the state of this from a provided Protobuf object.

        :param metadata_request: The Protobuf object.
        :type metadata_request: CollectionMetadataRequest_pb2.CollectionMetadataRequest
        """
        self._api_key = metadata_request.apiKey
        self._source = metadata_request.source
        self._code = metadata_request.code
        self._cid = metadata_request.id
        self._client_type = metadata_request.clientType

    def _write_proto_object(self) -> CollectionMetadataRequest_pb2.CollectionMetadataRequest:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: CollectionMetadataRequest_pb2.CollectionMetadataRequest
        """
        request = CollectionMetadataRequest_pb2.CollectionMetadataRequest()
        request.apiKey = self._api_key
        request.source = self._source
        request.code = self._code
        request.id = self._cid
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


class CollectionMetadataResponse:
    """
    Represents the response to a collection metadata request.
    """
    def __init__(self,
                 metadata: CollectionMetadata = None,
                 error_code: int = None,
                 error_message: str = None):
        """
        Either error_code and error_message should be supplied (with metadata None), or just metadata.

        :param metadata: The data to return.
        :type metadata: CollectionMetadata

        :param error_code: The error code.
        :type error_code: int

        :param error_message: The error message.
        :type error_message: str
        """
        if error_code is None:
            if not isinstance(metadata, CollectionMetadata):
                raise ValueError("metadata is not an instance of CollectionMetadata")

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
    def metadata(self) -> CollectionMetadata:
        """
        Returns the data to return if an error did not occur, None otherwise.

        :return: The data to return if an error did not occur, None otherwise.
        :rtype: CollectionMetadata
        """
        return self._metadata

    @staticmethod
    def deserialize(serialized: bytes) -> CollectionMetadataResponse:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a bytes created by serialize().
        :rtype: CollectionMetadataResponse
        """
        response = CollectionMetadataResponse(error_code=0, error_message="")
        response._read_proto(serialized)
        return response

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        response = CollectionMetadataResponse_pb2.CollectionMetadataResponse()
        response.ParseFromString(byte_array)
        self._read_proto_object(response)

    def _read_proto_object(self,
                           response: CollectionMetadataResponse_pb2.CollectionMetadataResponse):
        """
        Sets the state of this from a provided Protobuf object.

        :param response: The Protobuf object.
        :type response: CollectionMetadataResponse_pb2.CollectionMetadataResponse
        """
        self._error_occurred = response.errorHasOccurred

        if self._error_occurred:
            self._error_code = response.errorCode
            self._error_message = response.errorMessage
            self._metadata = None
        else:
            self._error_code = 0
            self._error_message = None
            self._metadata = CollectionMetadata("a", "a", "a", "", "", "", dict(), dict(), False, Timestamp.now(), Timestamp.now())
            self._metadata._read_proto_object(response.metadata)

    def _write_proto_object(self) -> CollectionMetadataResponse_pb2.CollectionMetadataResponse:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: CollectionMetadataRequest_pb2.CollectionMetadataRequest
        """
        response = CollectionMetadataResponse_pb2.CollectionMetadataResponse()
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


class CollectionRequest:
    """
    Represents a collection request.
    """
    def __init__(self,
                 source: str,
                 code: str,
                 cid: str,
                 features: List[str] = None,
                 max_size: int = -1,
                 filters: Dict[str, str] = None,
                 api_key: str = None):
        """
        :param source: The source for the collection.
        :type source: str

        :param code: The code for the collection.
        :type code: str

        :param cid: The ID for the collection.
        :type cid: str

        :param features: The (optional) list of features, or None.
        :type features: List[str]

        :param max_size: The (optional) maximum number of items that can be returned, or -1 if there should be no limit.
        :type max_size: int

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

        if not isinstance(cid, str):
            raise ValueError("cid is not a valid str")

        if not is_valid_token(cid):
            raise ValueError("cid is not valid")

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

        if filters is None:
            filters = {}

        if not isinstance(filters, Dict):
            raise ValueError("filters is not a dict")

        for feature_name in filters.keys():
            if not isinstance(feature_name, str):
                raise ValueError("filters does not contain only instances of str ")
            elif not is_valid_token(feature_name):
                raise ValueError("\"{}\" is not a valid name for a feature".format(feature_name))

            feature_filter = filters[feature_name]
            if not isinstance(feature_filter, str):
                raise ValueError("filters does not contain only instances of str ")

        # Store the data

        self._api_key = api_key
        self._source = source
        self._code = code
        self._cid = cid
        self._features = features
        self._max_size = max_size
        self._filters = filters
        self._client_type = ClientType.PYTHON_CLIENT

    @property
    def api_key(self) -> str or None:
        """
        Returns the API Key.

        :return:  The API Key.
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        """
         Sets a new value for the API Key.

        :param value: The new value for the API Key.
        :type value:
        """
        if value is not None and not isinstance(value, str):
            raise ValueError("value is not None or a valid str")

        self._api_key = value

    @property
    def source(self) -> str:
        """
        Returns the source for the collection.

        :return: The source for the collection.
        :rtype: str
        """
        return self._source

    @property
    def code(self) -> str:
        """
        Returns the code for the collection.

        :return: The code for the collection.
        :rtype: str
        """
        return self._code

    @property
    def cid(self) -> str:
        """
        Returns the ID for the collection.

        :return: The ID for the collection.
        :rtype: str
        """
        return self._cid

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
    def deserialize(serialized: bytes):
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: CollectionRequest
        """
        request = CollectionRequest("a", "a", "a", ["Example"], -1, {}, "a")
        request._read_proto(serialized)
        return request

    def _read_proto(self,
                    serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        Parameters
        ----------
        serialized : str or bytes
           The str produced by serialize().

        :param : .
        :type :
        """
        byte_array = array.array('B', serialized)
        request = CollectionRequest_pb2.CollectionRequest()
        request.ParseFromString(byte_array)
        self._read_proto_object(request)

    def _read_proto_object(self,
                           request: CollectionRequest_pb2.CollectionRequest):
        """
        Sets the state of this from a provided Protobuf object.

        :param request: The Protobuf object.
        :type request: CollectionRequest_pb2.CollectionRequest
        """
        self._api_key = request.apiKey
        self._source = request.source
        self._code = request.code
        self._cid = request.id

        if request.featuresSet:
            self._features = request.features
        else:
            self._features = None

        self._max_size = request.maxSize
        self._filters = request.filters
        self._client_type = request.clientType

    def _write_proto_object(self) -> CollectionRequest_pb2.CollectionRequest:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: CollectionRequest_pb2.CollectionRequest
        """
        request = CollectionRequest_pb2.CollectionRequest()
        request.apiKey = self._api_key
        request.source = self._source
        request.code = self._code
        request.id = self._cid

        if self._features is not None:
            request.featuresSet = True

            for item in self.features:
                request.features.append(item)
        else:
            request.featuresSet = False

        request.maxSize = self._max_size
        request.filters.update(self._filters)
        request.clientType = ClientType.PYTHON_CLIENT

        return request

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return: A bytes containing the state of this serialised.
        :rtype: bytes
        """
        request = self._write_proto_object()
        return request.SerializeToString()


class CollectionResponse:
    """
    Represents the response to a collection request.
    """
    def __init__(self,
                 data: Collection = None,
                 error_code: int = None,
                 error_message: str = None):
        """
        Either error_code and error_message should be supplied (with data None), or just data.

        :param data: The data to return.
        :type data: Collection

        :param error_code: The error code.
        :type error_code: int

        :param error_message: The error message.
        :type error_message: str
        """
        if error_code is None:
            if not isinstance(data, Collection):
                raise ValueError("data is not an instance of Collection")

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
        Returns if an error occurred then the error code, 0 otherwise.

        :return: If an error occurred then the error code, 0 otherwise.
        :rtype: int
        """
        return self._error_code

    @property
    def error_message(self) -> str:
        """
        Returns if an error occurred then the error message, None otherwise.

        :return: If an error occurred then the error message, None otherwise.
        :rtype: str
        """
        return self._error_message

    @property
    def data(self) -> Collection:
        """
        Returns if an error did not occur then the data to return, None otherwise.

        :return: If an error did not occur then the data to return, None otherwise.
        :rtype: Collection
        """
        return self._data

    @staticmethod
    def deserialize(serialized: bytes) -> CollectionResponse:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: CollectionResponse
        """
        response = CollectionResponse(error_code=0, error_message="")
        response._read_proto(serialized)
        return response

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        response = CollectionResponse_pb2.CollectionResponse()
        response.ParseFromString(byte_array)
        self._read_proto_object(response)

    def _read_proto_object(self, response: CollectionResponse_pb2.CollectionResponse):
        """
        Sets the state of this from a provided Protobuf object.

        :param response: The Protobuf object.
        :type response: CollectionResponse_pb2.CollectionResponse
        """
        self._error_occurred = response.errorHasOccurred

        if self._error_occurred:
            self._error_code = response.errorCode
            self._error_message = response.errorMessage
            self._data = None
        else:
            self._error_code = 0
            self._error_message = None
            self._data = Collection(CollectionMetadata("a", "a", "a", "", "", "", dict(), dict(), False, Timestamp.now(), Timestamp.now()), CollectionData({}))
            self._data._read_proto_object(response.collection)

    def _write_proto_object(self) -> CollectionResponse_pb2.CollectionResponse:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: CollectionResponse_pb2.CollectionResponse
        """
        response = CollectionResponse_pb2.CollectionResponse()
        response.errorHasOccurred = self._error_occurred

        if self._error_occurred:
            response.errorCode = self._error_code
            response.errorMessage = self._error_message
        else:
            response.collection.CopyFrom(self._data._write_proto_object())

        return response

    def serialize(self) -> bytes:
        """
        Serializes the state of this as a bytes.

        :return: A bytes containing the state of this serialised.
        :rtype: bytes
        """
        response = self._write_proto_object()
        return response.SerializeToString()
