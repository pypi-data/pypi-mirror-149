"""
Contains classes and functions related to file stores.
"""
from __future__ import annotations
from typing import List, Dict

from archipelagos.common.data import get_secs_from_timestamp, get_nanos_from_timestamp, get_timestamp
from archipelagos.common.data import get_yyyy_mm_dd_hh_mm_ss_n
from archipelagos.common.protobuf.common.data.filestore import FileStoreRequest_pb2, FileStoreResponse_pb2
from archipelagos.common.protobuf.common.data.filestore import FileStoreMetadataResponse_pb2
from archipelagos.common.protobuf.common.data.filestore import FileStoreMetadataRequest_pb2
from archipelagos.common.protobuf.common.data.filestore import FileMetadataResponse_pb2
from archipelagos.common.protobuf.common.data.filestore import FileMetadataRequest_pb2
from archipelagos.common.protobuf.common.data.filestore import FileStoreMetadata_pb2, FileMetadata_pb2
from archipelagos.common.protobuf.common import Timestamp_pb2
from archipelagos.common.platform import ClientType

from archipelagos.common.data import is_valid_token

import array
from pandas import Timestamp


class FileStoreMetadata:
    """
    Represents the metadata about a file store.
    """
    def __init__(self,
                 source: str,
                 code: str,
                 fs_id: str,
                 url: str,
                 summary: str,
                 description: str,
                 properties: Dict[str, str],
                 premium: bool,
                 created: Timestamp,
                 edited: Timestamp or None = None):
        """
        All parameters should be supplied unless deserializing an object.

        :param source: The source for the file store.
        :type source: str

        :param code: The code for the file store.
        :type code: str

        :param fs_id: The ID for the file store.
        :type fs_id: str

        :param url: The URL for the file store.
        :type url: str

        :param summary: The summary for the file store.
        :type summary: str

        :param description: The description for the file store.
        :type description: str

        :param properties: The file store's properties.
        :type properties: Dict[str, str]

        :param premium: True if the file store is premium, false otherwise.
        :type premium: bool

        :param created: When (in UTC) the file store was created.
        :type created: Timestamp

        :param edited: When (in UTC) the metadata for the file store was last edited.
        :type edited: Timestamp or None
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

        if not isinstance(fs_id, str):
            raise ValueError("fs_id is not a valid str")

        if not is_valid_token(fs_id):
            raise ValueError("fs_id is not valid")

        if not isinstance(url, str):
            raise ValueError("url is not a valid str")

        if not isinstance(summary, str):
            raise ValueError("summary is not a valid str")

        if not isinstance(description, str):
            raise ValueError("description is not a valid str")

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

        if edited is None:
            edited = created
        else:
            if not isinstance(edited, Timestamp):
                raise ValueError("edited is not a valid Timestamp")

        if edited < created:
            raise ValueError("edited is before created")

        # Store the data

        self._source = source
        self._code = code
        self._fs_id = fs_id
        self._url = url
        self._summary = summary
        self._description = description
        self._properties = properties
        self._premium = premium
        self._created = created
        self._edited = edited

        self._build_hash_code()

    def _build_hash_code(self):
        """
        Calculates and caches the hash code associated with this.
        """
        prime = 31
        result = 1

        result = prime * result + hash(self._source) if self._source is not None else 0
        result = prime * result + hash(self._code) if self._code is not None else 0
        result = prime * result + hash(self._fs_id) if self._fs_id is not None else 0

        self._hash_code = result

    @property
    def source(self) -> str:
        """
        Returns the source for the file store.

        :return: The source for the file store.
        :rtype: str
        """
        return self._source

    @property
    def code(self) -> str:
        """
        Returns the code for the file store.

        :return: The code for the file store.
        :rtype: str
        """
        return self._code

    @property
    def fs_id(self) -> str:
        """
        Returns the ID for the file store.

        :return: The ID for the file store.
        :rtype: str
        """
        return self._fs_id

    @property
    def url(self) -> str:
        """
        Returns the url for the file store.

        :return: The url for the file store.
        :rtype: str
        """
        return self._url

    @property
    def summary(self) -> str:
        """
        Returns the summary for the file store.

        :return: The summary for the file store.
        :rtype: str
        """
        return self._summary

    @property
    def description(self) -> str:
        """
        Returns the description for the file store.

        :return: The description for the file store.
        :rtype: str
        """
        return self._description

    @property
    def properties(self) -> Dict[str, str]:
        """
        Returns the file store's properties.

        :return: The file store's properties.
        :rtype: Dict[str, str]
        """
        return self._properties

    @property
    def premium(self) -> bool:
        """
        Returns True if the file store is premium, False otherwise.

        :return: True if the file store is premium, False otherwise.
        :rtype: bool
        """
        return self._premium

    @property
    def created(self) -> Timestamp:
        """
        Returns when (in UTC) the file store was created.

        :return: When (in UTC) the file store was created.
        :rtype: Timestamp
        """
        return self._created

    @property
    def edited(self) -> Timestamp:
        """
        Returns when (in UTC) the metadata for the file store was last edited.

        :return: When (in UTC) the metadata for the file store was last edited.
        :rtype: Timestamp
        """
        return self._edited

    @staticmethod
    def deserialize(serialized: bytes) -> FileStoreMetadata:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: FileStoreMetadata
        """
        metadata = FileStoreMetadata("a", "a", "a", "", "", "", dict(), False, Timestamp.now(), Timestamp.now())
        metadata._read_proto(serialized)
        return metadata

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        metadata = FileStoreMetadata_pb2.FileStoreMetadata()
        metadata.ParseFromString(byte_array)
        self._read_proto_object(metadata)

    def _read_proto_object(self, metadata: FileStoreMetadata_pb2.FileStoreMetadata):
        """
        Sets the state of this from a provided Protobuf object.

        :param metadata: The Protobuf object.
        :type metadata: FileStoreMetadata_pb2.FileStoreMetadata
        """
        self._source = metadata.source
        self._code = metadata.code
        self._fs_id = metadata.id
        self._url = metadata.url
        self._summary = metadata.summary
        self._description = metadata.description
        self._premium = metadata.premium

        timestamp = metadata.created
        self._created = get_timestamp(timestamp.epochSecond, timestamp.nanosecond)

        timestamp = metadata.edited
        self._edited = get_timestamp(timestamp.epochSecond, timestamp.nanosecond)

        self._build_hash_code()

    def _write_proto_object(self) -> FileStoreMetadata_pb2.FileStoreMetadata:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: FileStoreMetadata_pb2.FileStoreMetadata
        """
        metadata = FileStoreMetadata_pb2.FileStoreMetadata()
        metadata.source = self._source
        metadata.code = self._code
        metadata.id = self._fs_id
        metadata.url = self._url
        metadata.summary = self._summary
        metadata.description = self._description
        metadata.premium = self._premium

        timestamp = Timestamp_pb2.Timestamp()
        timestamp.epochSecond = get_secs_from_timestamp(self._created)
        timestamp.nanosecond = get_nanos_from_timestamp(self._created)
        metadata.created.CopyFrom(timestamp)

        timestamp = Timestamp_pb2.Timestamp()
        timestamp.epochSecond = get_secs_from_timestamp(self._edited)
        timestamp.nanosecond = get_nanos_from_timestamp(self._edited)
        metadata.edited.CopyFrom(timestamp)

        return metadata

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return: A bytes containing the state of this serialised.
        :rtype: bytes
        """
        metadata = self._write_proto_object()
        return metadata.SerializeToString()

    def __eq__(self, other):
        if isinstance(other, FileStoreMetadata):
            if self._source is None and other._source is not None:
                return False
            elif self._source != other._source:
                return False

            if self._code is None and other._code is not None:
                return False
            elif self._code != other._code:
                return False

            if self._fs_id is None and other._fs_id is not None:
                return False
            elif self._fs_id != other._fs_id:
                return False

            return True

        return False

    def __hash__(self):
        return self._hash_code

    def __str__(self):
        return "Source = " + self._source + \
               "Code = " + self._code + \
               "ID = " + self._fs_id + \
               "URL = " + self._url + \
               "Summary = " + self._summary + \
               "Description = " + self._description + \
               "Premium = " + str(self._premium) + \
               "Created = " + get_yyyy_mm_dd_hh_mm_ss_n(self._created) + \
               "Edited = " + get_yyyy_mm_dd_hh_mm_ss_n(self._edited)


class FileMetadata:
    """
    Represents the metadata about a file in a file store.
    """
    def __init__(self,
                 source: str,
                 code: str,
                 fs_id: str,
                 name: str,
                 size: int,
                 premium: bool,
                 created: Timestamp = None):
        """
        All parameters should be supplied unless deserializing an object.

        :param source: The source for the file store.
        :type source: str

        :param code: The code for the file store.
        :type code: str

        :param fs_id: The ID for the file store.
        :type fs_id: str

        :param name: The name of the file.
        :type name: str

        :param size: The size of the file in bytes.
        :type size: int

        :param premium: True if the file is premium, False otherwise.
        :type premium: bool

        :param created: When (in UTC) the file was created.
        :type created: Timestamp
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

        if not isinstance(fs_id, str):
            raise ValueError("fs_id is not a valid str")

        if not is_valid_token(fs_id):
            raise ValueError("fs_id is not valid")

        if not isinstance(name, str):
            raise ValueError("name is not a valid str")

        if not isinstance(size, int):
            raise ValueError("size is not an int")

        if not isinstance(premium, bool):
            raise ValueError("premium is not a valid bool")

        if not isinstance(created, Timestamp):
            raise ValueError("created is not a valid Timestamp")

        # Store the data

        self._source = source
        self._code = code
        self._fs_id = fs_id
        self._name = name
        self._size = size
        self._premium = premium
        self._created = created

        self._build_hash_code()

    def _build_hash_code(self):
        """
        Calculates and caches the hash code associated with this.
        """

        prime = 31
        result = 1

        result = prime * result + hash(self._source) if self._source is not None else 0
        result = prime * result + hash(self._code) if self._code is not None else 0
        result = prime * result + hash(self._fs_id) if self._fs_id is not None else 0
        result = prime * result + hash(self._name) if self._name is not None else 0

        self._hash_code = result

    @property
    def source(self) -> str:
        """
        Returns the source for the file store.

        :return: The source for the file store.
        :rtype: str
        """
        return self._source

    @property
    def code(self) -> str:
        """
        Returns the code for the file store.

        :return: The code for the file store.
        :rtype: str
        """
        return self._code

    @property
    def fs_id(self) -> str:
        """
        Returns the ID for the file store.

        :return: The ID for the file store.
        :rtype: str
        """
        return self._fs_id

    @property
    def name(self) -> str:
        """
        Returns the name for the file.

        :return: The name for the file.
        :rtype: str
        """
        return self._name

    @property
    def size(self) -> int:
        """
        Returns the size of the file in bytes.

        :return: The size of the file in bytes.
        :rtype: int
        """
        return self._size

    @property
    def premium(self) -> bool:
        """
        Returns True if the file store is premium, False otherwise.

        :return: True if the file store is premium, False otherwise.
        :rtype: bool
        """
        return self._premium

    @property
    def created(self) -> Timestamp:
        """
        Returns when (in UTC) the file was created.

        :return: When (in UTC) the file was created.
        :rtype: Timestamp
        """
        return self._created

    @staticmethod
    def deserialize(serialized: bytes) -> FileMetadata:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: FileMetadata
        """
        metadata = FileMetadata("a", "a", "a", "", 0, False, Timestamp.now())
        metadata._read_proto(serialized)
        return metadata

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        metadata = FileMetadata_pb2.FileMetadata()
        metadata.ParseFromString(byte_array)
        self._read_proto_object(metadata)

    def _read_proto_object(self,
                           metadata: FileMetadata_pb2.FileMetadata):
        """
        Sets the state of this from a provided Protobuf object.

        :param metadata: The Protobuf object.
        :type metadata: FileMetadata_pb2.FileMetadata
        """
        self._source = metadata.source
        self._code = metadata.code
        self._fs_id = metadata.id
        self._name = metadata.name
        self._size = metadata.size
        self._premium = metadata.premium

        timestamp = metadata.created
        self._created = get_timestamp(timestamp.epochSecond, timestamp.nanosecond)

        self._build_hash_code()

    def _write_proto_object(self) -> FileMetadata_pb2.FileMetadata:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: FileMetadata_pb2.FileMetadata
        """
        metadata = FileMetadata_pb2.FileMetadata()
        metadata.source = self._source
        metadata.code = self._code
        metadata.id = self._fs_id
        metadata.name = self._name
        metadata.size = self._size
        metadata.premium = self._premium

        timestamp = Timestamp_pb2.Timestamp()
        timestamp.epochSecond = get_secs_from_timestamp(self._created)
        timestamp.nanosecond = get_nanos_from_timestamp(self._created)
        metadata.created.CopyFrom(timestamp)

        return metadata

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return: A bytes containing the state of this serialised.
        :rtype: bytes
        """
        metadata = self._write_proto_object()
        return metadata.SerializeToString()

    def __eq__(self, other):
        if isinstance(other, FileMetadata):
            if self._source is None and other._source is not None:
                return False
            elif self._source != other._source:
                return False

            if self._code is None and other._code is not None:
                return False
            elif self._code != other._code:
                return False

            if self._fs_id is None and other._fs_id is not None:
                return False
            elif self._fs_id != other._fs_id:
                return False

            if self._name is None and other._name is not None:
                return False
            elif self._name != other._name:
                return False

            return True

        return False

    def __hash__(self):
        return self._hash_code

    def __str__(self):
        return "Source = " + self._source + \
               "Code = " + self._code + \
               "ID = " + self._fs_id + \
               "Name = " + self._name + \
               "Size = " + str(self._size) + \
               "Premium = " + str(self._premium) + \
               "Created = " + get_yyyy_mm_dd_hh_mm_ss_n(self._created)


class FileStoreMetadataRequest:
    """
    Represents a file store metadata request.
    """
    def __init__(self,
                 source: str,
                 code: str,
                 fs_id: str,
                 api_key: str = None):
        """
        All parameters should be supplied unless deserializing an object.

        :param source: The source for the file store.
        :type source: str

        :param code: The code for the file store.
        :type code: str

        :param fs_id: The ID for the file store.
        :type fs_id: str

        :param api_key: The API Key.
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

        if not isinstance(fs_id, str):
            raise ValueError("fs_id is not a valid str")

        if not is_valid_token(fs_id):
            raise ValueError("fs_id is not valid")

        # Store the data

        self._api_key = api_key
        self._source = source
        self._code = code
        self._fs_id = fs_id
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
        Returns the source for the file store.

        :return: The source for the file store.
        :rtype: str
        """
        return self._source

    @property
    def code(self) -> str:
        """
        Returns the code for the file store.

        :return: The code for the file store.
        :rtype: str
        """
        return self._code

    @property
    def fs_id(self) -> str:
        """
        Returns the ID for the file store.

        :return: The ID for the file store.
        :rtype: str
        """
        return self._fs_id

    @property
    def client_type(self) -> str:
        """
        Returns the type of client that sent the request.

        :return: The type of client that sent the request.
        :rtype: str
        """
        return self._client_type

    @staticmethod
    def deserialize(serialized: bytes) -> FileStoreMetadataRequest:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: FileStoreMetadataRequest
        """
        request = FileStoreMetadataRequest("a", "a", "a", "a")
        request._read_proto(serialized)
        return request

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        request = FileStoreMetadataRequest_pb2.FileStoreMetadataRequest()
        request.ParseFromString(byte_array)
        self._read_proto_object(request)

    def _read_proto_object(self, metadata_request: FileStoreMetadataRequest_pb2.FileStoreMetadataRequest):
        """
        Sets the state of this from a provided Protobuf object.

        :param metadata_request: The Protobuf object.
        :type metadata_request: FileStoreMetadataRequest_pb2.FileStoreMetadataRequest
        """
        self._api_key = metadata_request.apiKey
        self._source = metadata_request.source
        self._code = metadata_request.code
        self._fs_id = metadata_request.id
        self._client_type = metadata_request.clientType

    def _write_proto_object(self) -> FileStoreMetadataRequest_pb2.FileStoreMetadataRequest:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: FileStoreMetadataRequest_pb2.FileStoreMetadataRequest
        """
        request = FileStoreMetadataRequest_pb2.FileStoreMetadataRequest()
        request.apiKey = self._api_key
        request.source = self._source
        request.code = self._code
        request.id = self._fs_id
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


class FileStoreMetadataResponse:
    """
    Represents the response to a file store metadata request.
    """
    def __init__(self,
                 metadata: FileStoreMetadata = None,
                 error_code: int = None,
                 error_message: str = None):
        """
        Either error_code and error_message should be supplied (with metadata None), or just metadata.

        :param metadata: The data to return.
        :type metadata: FileStoreMetadata

        :param error_code: The error code.
        :type error_code: int

        :param error_message: The error message.
        :type error_message: str
        """
        if error_code is None:
            if not isinstance(metadata, FileStoreMetadata):
                raise ValueError("metadata is not an instance of FileStoreMetadata")

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
        Returns the error code if an error occurred then the error code, 0 otherwise.

        :return: The error code if an error occurred then the error code, 0 otherwise.
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
    def metadata(self) -> FileStoreMetadata:
        """
        Returns the data to return if an error did not occur, None otherwise.

        :return: The data to return if an error did not occur, None otherwise.
        :rtype: FileStoreMetadata
        """
        return self._metadata

    @staticmethod
    def deserialize(serialized: bytes) -> FileStoreMetadataResponse:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: FileStoreMetadataResponse
        """
        response = FileStoreMetadataResponse(error_code=0, error_message="")
        response._read_proto(serialized)
        return response

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        response = FileStoreMetadataResponse_pb2.FileStoreMetadataResponse()
        response.ParseFromString(byte_array)
        self._read_proto_object(response)

    def _read_proto_object(self,
                           response: FileStoreMetadataResponse_pb2.FileStoreMetadataResponse):
        """
        Sets the state of this from a provided Protobuf object.

        :param response: The Protobuf object.
        :type response: FileStoreMetadataResponse_pb2.FileStoreMetadataResponse
        """
        self._error_occurred = response.errorHasOccurred

        if self._error_occurred:
            self._error_code = response.errorCode
            self._error_message = response.errorMessage
            self._metadata = None
        else:
            self._error_code = 0
            self._error_message = None
            self._metadata = FileStoreMetadata("a", "a", "a", "", "", "", dict(), False, Timestamp.now(), Timestamp.now())
            self._metadata._read_proto_object(response.metadata)

    def _write_proto_object(self) -> FileStoreMetadataResponse_pb2.FileStoreMetadataResponse:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: FileStoreMetadataRequest_pb2.FileStoreMetadataRequest
        """
        response = FileStoreMetadataResponse_pb2.FileStoreMetadataResponse()
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


class FileStoreRequest:
    """
    Represents a file store request.
    """
    def __init__(self,
                 source: str,
                 code: str,
                 fs_id: str,
                 name: str,
                 api_key: str = None):
        """
        :param source: The source for the file store.
        :type source: str

        :param code: The code for the file store.
        :type code: str

        :param fs_id: The ID of the file.
        :type fs_id: str

        :param name: The name of the file.
        :type name: str

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

        if not isinstance(fs_id, str):
            raise ValueError("fs_id is not a valid str")

        if not is_valid_token(fs_id):
            raise ValueError("fs_id is not valid")

        if not isinstance(name, str):
            raise ValueError("name is not a valid str")

        # Store the data

        self._api_key = api_key
        self._source = source
        self._code = code
        self._fs_id = fs_id
        self._name = name
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
    def api_key(self, value: str):
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
        Returns the source for the file store.

        :return: The source for the file store.
        :rtype: str
        """
        return self._source

    @property
    def code(self) -> str:
        """
        Returns the code for the file store.

        :return: The code for the file store.
        :rtype: str
        """
        return self._code

    @property
    def fs_id(self) -> str:
        """
        Returns the ID for the file store.

        :return: The ID for the file store.
        :rtype: str
        """
        return self._fs_id

    @property
    def name(self) -> str:
        """
        Returns the name for the file.

        :return: The name for the file.
        :rtype: str
        """
        return self._name

    @property
    def client_type(self) -> str:
        """
        Returns the type of client that sent the request.

        :return: The type of client that sent the request.
        :rtype: str
        """
        return self._client_type

    @staticmethod
    def deserialize(serialized: bytes) -> FileStoreRequest:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: FileStoreRequest
        """
        request = FileStoreRequest("a", "a", "a", "a", "a")
        request._read_proto(serialized)
        return request

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        request = FileStoreRequest_pb2.FileStoreRequest()
        request.ParseFromString(byte_array)
        self._read_proto_object(request)

    def _read_proto_object(self, request: FileStoreRequest_pb2.FileStoreRequest):
        """
        Sets the state of this from a provided Protobuf object.

        :param request: The Protobuf object.
        :type request: FileStoreRequest_pb2.FileStoreRequest
        """
        self._api_key = request.apiKey
        self._source = request.source
        self._code = request.code
        self._fs_id = request.id
        self._name = request.name
        self._client_type = request.clientType

    def _write_proto_object(self) -> FileStoreRequest_pb2.FileStoreRequest:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: FileStoreRequest_pb2.FileStoreRequest
        """
        request = FileStoreRequest_pb2.FileStoreRequest()
        request.apiKey = self._api_key
        request.source = self._source
        request.code = self._code
        request.id = self._fs_id
        request.name = self._name
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


class FileStoreResponse:
    """
    Represents the response to a files store request.
    """
    def __init__(self,
                 file: bytes = None,
                 metadata: FileMetadata = None,
                 error_code: int = None,
                 error_message: str = None):
        """
        Either error_code and error_message should be supplied (with data None), or just data.

        :param file: The file to return.
        :type file: bytes

        :param metadata: The file to return.
        :type metadata: FileMetadata

        :param error_code: The error code.
        :type error_code: int

        :param error_message: The error message.
        :type error_message: str
        """
        if error_code is None:
            if not isinstance(file, bytes):
                raise ValueError("file is not an instance of bytes")

            if not isinstance(metadata, FileMetadata):
                raise ValueError("metadata is not an instance of FileMetadata")

            if error_message is not None:
                raise ValueError("error_code is None and error_message is not None")

            self._error_occurred = False
            self._error_code = 0
            self._error_message = None
            self._file = file
            self._metadata = metadata

        else:
            if not isinstance(error_code, int):
                raise ValueError("error_code is not None and is not a valid int")

            if not isinstance(error_message, str):
                raise ValueError("error_code is not None and error_message is not a valid str")

            if file is not None:
                raise ValueError("error_code is not None and file is not None")

            if metadata is not None:
                raise ValueError("error_code is not None and metadata is not None")

            self._error_occurred = True
            self._error_code = error_code
            self._error_message = error_message
            self._file = file
            self._metadata = metadata

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
    def file(self) -> bytes:
        """
        Returns the file to return if an error did not occur, None otherwise.

        :return: The file to return if an error did not occur, None otherwise.
        :rtype: bytes
        """
        return self._file

    @property
    def metadata(self) -> FileMetadata:
        """
        Returns the metadata for the file to return if an error did not occur, None otherwise.

        :return: The metadata for the file to return if an error did not occur, None otherwise.
        :rtype: bytes
        """
        return self._metadata

    @staticmethod
    def deserialize(serialized: bytes) -> FileStoreResponse:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: FileStoreResponse
        """
        response = FileStoreResponse(error_code=0, error_message="")
        response._read_proto(serialized)
        return response

    def _read_proto(self, serialized: bytes):
        """
        Sets the state of this from a str containing the state of an object serialised using Protobuf.

        :param serialized: The str produced by serialize().
        :type serialized: bytes
        """
        byte_array = array.array('B', serialized)
        response = FileStoreResponse_pb2.FileStoreResponse()
        response.ParseFromString(byte_array)
        self._read_proto_object(response)

    def _read_proto_object(self,
                           response: FileStoreResponse_pb2.FileStoreResponse):
        """
        Sets the state of this from a provided Protobuf object.

        :param response: The Protobuf object.
        :type response: FileStoreResponse_pb2.FileStoreResponse
        """
        self._error_occurred = response.errorHasOccurred

        if self._error_occurred:
            self._error_code = response.errorCode
            self._error_message = response.errorMessage
            self._file = None
            self._metadata = None
        else:
            self._error_code = 0
            self._error_message = None
            self._metadata = FileMetadata("a", "a", "a", "a", 0, False, Timestamp.now())
            self._metadata._read_proto_object(response.metadata)
            self._file = response.file

    def _write_proto_object(self) -> FileStoreResponse_pb2.FileStoreResponse:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: FileStoreResponse_pb2.FileStoreResponse
        """
        response = FileStoreResponse_pb2.FileStoreResponse()
        response.errorHasOccurred = self._error_occurred

        if self._error_occurred:
            response.errorCode = self._error_code
            response.errorMessage = self._error_message
        else:
            response.file = self._file
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


class FileMetadataRequest:
    """Represents a file metadata request.
    """
    def __init__(self,
                 source: str,
                 code: str,
                 fs_id: str,
                 pattern: str = None,
                 api_key: str = None):
        """
        All parameters should be supplied unless deserializing an object.

        :param source: The source for the file store.
        :type source: str

        :param code: The code for the file store.
        :type code: str

        :param fs_id: The ID for the file store.
        :type fs_id: str

        :param pattern: The pattern that the name of a file whose metadata is returned should match; None will match all files.
        :type pattern: str

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

        if not isinstance(fs_id, str):
            raise ValueError("fs_id is not a valid str")

        if not is_valid_token(fs_id):
            raise ValueError("fs_id is not valid")

        # Store the data

        self._api_key = api_key
        self._source = source
        self._code = code
        self._fs_id = fs_id
        self._pattern = pattern
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
    def api_key(self, value: str):
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
        Returns the source for the file store.

        :return: The source for the file store.
        :rtype: str
        """
        return self._source

    @property
    def code(self) -> str:
        """
        Returns the code for the file store.

        :return: The code for the file store.
        :rtype: str
        """
        return self._code

    @property
    def fs_id(self) -> str:
        """
        Returns the ID for the file store.

        :return: The ID for the file store.
        :rtype: str
        """
        return self._fs_id

    @property
    def pattern(self) -> str:
        """
        Returns the pattern that the name of a file whose metadata is returned should match; None will match all files.

        :return: The pattern that the name of a file whose metadata is returned should match; None will match all files.
        :rtype: The pattern that the name of a file whose metadata is returned should match; None will match all files.
        """
        return self._pattern

    @property
    def client_type(self) -> str:
        """
        Returns the type of client that sent the request.

        :return: The type of client that sent the request.
        :rtype: str
        """
        return self._client_type

    @staticmethod
    def deserialize(serialized: bytes) -> FileMetadataRequest:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: FileMetadataRequest
        """
        request = FileMetadataRequest("a", "a", "a", "a", "a")
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
        request = FileMetadataRequest_pb2.FileMetadataRequest()
        request.ParseFromString(byte_array)
        self._read_proto_object(request)

    def _read_proto_object(self,
                           metadata_request: FileMetadataRequest_pb2.FileMetadataRequest):
        """
        Sets the state of this from a provided Protobuf object.

        :param metadata_request: The Protobuf object.
        :type metadata_request: FileMetadataRequest_pb2.FileMetadataRequest
        """
        self._api_key = metadata_request.apiKey
        self._source = metadata_request.source
        self._code = metadata_request.code
        self._fs_id = metadata_request.id
        self._client_type = metadata_request.clientType

        if metadata_request.patternSet:
            self._pattern = metadata_request.pattern
        else:
            self._pattern = None

    def _write_proto_object(self) -> FileMetadataRequest_pb2.FileMetadataRequest:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: FileMetadataRequest_pb2.FileMetadataRequest
        """
        request = FileMetadataRequest_pb2.FileMetadataRequest()
        request.apiKey = self._api_key
        request.source = self._source
        request.code = self._code
        request.id = self.fs_id

        if self._pattern is None:
            request.patternSet = False
        else:
            request.patternSet = True
            request.pattern = self._pattern

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


class FileMetadataResponse:
    """
    Represents the response to a file metadata request.
    """
    def __init__(self,
                 metadata: List[FileMetadata] = None,
                 error_code: int = None,
                 error_message: str = None):
        """
        Either error_code and error_message should be supplied (with metadata None), or just metadata.

        :param metadata: The data to return.
        :type metadata: List[FileMetadata]

        :param error_code: The error code.
        :type error_code: int

        :param error_message: The error message.
        :type error_message: str
        """
        if error_code is None:
            if not isinstance(metadata, list):
                raise ValueError("metadata is not an instance of list")

            for file_metadata in metadata:
                if not isinstance(file_metadata, FileMetadata):
                    raise ValueError("metadata has one or more elements that are not instances of FileMetadata")

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
    def metadata(self) -> List[FileMetadata]:
        """
        Returns the data to return if an error did not occur, None otherwise.

        :return: The data to return if an error did not occur, None otherwise.
        :rtype: List[FileMetadata]
        """
        return self._metadata

    @staticmethod
    def deserialize(serialized: bytes) -> FileMetadataResponse:
        """
        Creates a new instance using a str created by serialize().

        :param serialized: The str produced by serialize().
        :type serialized: bytes

        :return: A new instance using a str created by serialize().
        :rtype: FileMetadataResponse
        """
        response = FileMetadataResponse(error_code=0, error_message="")
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
        response = FileMetadataResponse_pb2.FileMetadataResponse()
        response.ParseFromString(byte_array)
        self._read_proto_object(response)

    def _read_proto_object(self,
                           response: FileMetadataResponse_pb2.FileMetadataResponse):
        """
        Sets the state of this from a provided Protobuf object.

        :param response: The Protobuf object.
        :type response: FileMetadataResponse_pb2.FileMetadataResponse
        """
        self._error_occurred = response.errorHasOccurred

        if self._error_occurred:
            self._error_code = response.errorCode
            self._error_message = response.errorMessage
            self._metadata = None
        else:
            self._error_code = 0
            self._error_message = None
            self._metadata = list()

            for file_metadata_proto in response.metadata:
                file_metadata = FileMetadata("a", "a", "a", "", 0, False, Timestamp.now())
                file_metadata._read_proto_object(file_metadata_proto)
                self._metadata.append(file_metadata)

    def _write_proto_object(self) -> FileMetadataResponse_pb2.FileMetadataResponse:
        """
        Builds a Protobuf object containing the serialised state of this.

        :return: A Protobuf object containing the serialised state of this.
        :rtype: FileMetadataRequest_pb2.FileMetadataRequest
        """
        response = FileMetadataResponse_pb2.FileMetadataResponse()
        response.errorHasOccurred = self._error_occurred

        if self._error_occurred:
            response.errorCode = self._error_code
            response.errorMessage = self._error_message
        else:
            for file_metadata in self._metadata:
                response.metadata.append(file_metadata._write_proto_object())

        return response

    def serialize(self) -> bytes:
        """
        Returns a bytes containing the state of this serialised.

        :return: A bytes containing the state of this serialised.
        :rtype: bytes
        """
        response = self._write_proto_object()
        return response.SerializeToString()
