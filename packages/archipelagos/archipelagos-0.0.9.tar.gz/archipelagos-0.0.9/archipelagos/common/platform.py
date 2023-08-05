"""
Classes and functions useful across both the server and client side of the platform.
"""
from archipelagos.common.data import DataType


# The URL that the platform is located at

PLATFORM_URL = "https://www.archipelagos-labs.com"


class ReturnCodes:
    """
    The return codes used in the platform.
    """
    SUCCESS = 0
    UNEXPECTED_SYSTEM_ERROR = 1
    UNRECOGNISED_USER = 2
    INSUFFICIENT_PERMISSIONS = 3
    UNRECOGNISED_TIME_SERIES = 4
    UNSPECIFIED_FORMAT = 5
    UNRECOGNISED_FORMAT = 6
    UNSPECIFIED_SOURCE = 7
    UNSPECIFIED_CODE = 8
    UNSPECIFIED_ID = 9
    UNSPECIFIED_API_KEY = 10
    INVALID_MAX_SIZE = 11
    INVALID_START = 12
    INVALID_END = 13
    INVALID_FEATURES = 14
    INVALID_FLATTEN = 15
    INVALID_TYPE = 16
    INVALID_ORDER = 17
    TOO_MANY_CONCURRENT_REQUESTS = 18
    TOO_MANY_REQUESTS = 19
    UNRECOGNISED_COLLECTION = 20
    INVALID_FILTERS = 21
    UNRECOGNISED_FILE_STORE = 22
    UNRECOGNISED_FILE = 23
    INVALID_PATTERN = 24
    INVALID_FILENAME = 25


def get_url(data_type: DataType, source: str, code: str, did: str):
    """
    Generates the website URL for a specified dataset.

    :param data_type: The type of the data.
    :type data_type: DataType

    :param source: The source for the data.
    :type source: DataType

    :param code: The code for the data.
    :type code: str

    :param did: The ID for the data.
    :type did: str

    :return: The URL.
    :rtype: str
    """
    return PLATFORM_URL + "/" + str(data_type).lower() + "/" + source + "/" + code + "/" + did


class HttpConstants:
    """
    Constants when dealing with HTTP request/responses.
    """
    FORMAT_BINARY = "bin"
    FORMAT_JSON = "json"
    FORMAT_XML = "xml"
    FORMAT_CSV = "csv"
    TYPE_PARAMETER = "type"
    SOURCE_PARAMETER = "source"
    CODE_PARAMETER = "code"
    ID_PARAMETER = "id"
    API_KEY_PARAMETER = "api_key"
    START_PARAMETER = "start"
    END_PARAMETER = "end"
    FEATURES_PARAMETER = "features"
    MAX_SIZE_PARAMETER = "max_size"
    FORMAT_PARAMETER = "format"
    FLATTEN_PARAMETER = "flatten"
    ORDER_PARAMETER = "order"
    FILENAME_PARAMETER = "filename"
    PATTERN_PARAMETER = "pattern"
    ORDER_ASCENDING = "asc"
    ORDER_DESCENDING = "desc"
    TIME_SERIES_REQUEST = "time-series"
    TIME_SERIES_METADATA_REQUEST = "time-series-metadata"
    COLLECTION_REQUEST = "collection"
    COLLECTION_METADATA_REQUEST = "collection-metadata"
    FILE_STORE_REQUEST = "file-store"
    FILE_STORE_METADATA_REQUEST = "file-store-metadata"
    FILE_METADATA_REQUEST = "file-metadata"
    CLIENT_TYPE_PARAMETER = "archipelagos_client_type"


class ClientType:
    """
    The types of Client supported in the platform.
    """
    PYTHON_CLIENT = "Python Client"
    JAVA_CLIENT = "Java Client"
    CSHARP_CLIENT = "C# Client"
    HTTP_CLIENT = "HTTP Client"
    HTTP_PYTHON_CLIENT = "HTTP Client (Python)"
    HTTP_JAVA_CLIENT = "HTTP Client (Java)"
    HTTP_CSHARP_CLIENT = "HTTP Client (C#)"
