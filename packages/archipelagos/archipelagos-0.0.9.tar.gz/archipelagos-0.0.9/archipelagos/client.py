"""
The cLasses and functions that representing the Python Client.
"""
from archipelagos.common.data.collection import CollectionMetadataRequest, CollectionMetadataResponse
from archipelagos.common.data.collection import CollectionRequest, CollectionResponse
from archipelagos.common.data.filestore import FileStoreMetadataRequest, FileStoreMetadataResponse
from archipelagos.common.data.filestore import FileStoreResponse, FileStoreRequest
from archipelagos.common.data.filestore import FileMetadataRequest, FileMetadataResponse
from archipelagos.common.data.timeseries import TimeSeriesRequest, TimeSeriesResponse
from archipelagos.common.data.timeseries import TimeSeriesMetadataRequest, TimeSeriesMetadataResponse
from archipelagos.common.platform import HttpConstants, ClientType

import io
import pandas as pd
import numpy as np
from urllib.parse import urlparse, urlencode, parse_qsl, urlunparse
import requests
from typing import Dict, List, Any
from pandas import Timestamp


# Default location that the client will look for the platform.
# For development purposes HTTP_URL can be altered to http://localhost
# if the Data Service component is being run on the same machine.

HTTP_URL = "http://www.archipelagos-labs.com"
HTTP_PORT = 6725


# CLasses and functions

class PlatformError(Exception):
    """
    Represents an error thrown by the platform
    """
    def __init__(self, error_code: int, error_message: str):
        """
        :param error_code: The code representing the error that occurred.
        :type error_code: int

        :param error_message: The human readable message explaining the error.
        :type error_message: str
        """
        self._error_code = error_code
        self._error_message = error_message

    @property
    def error_code(self) -> int:
        """
        Returns the code representing the error that occurred.

        :return: The code representing the error that occurred..
        :rtype: int
        """
        return self._error_code

    @property
    def error_message(self) -> str:
        """
        Returns the human readable message explaining the error.

        :return: The human readable message explaining the error.
        :rtype: str
        """
        return self._error_message


class Archipelagos:
    """
    The entry point for the functionality provided by the platform.
    """
    _http_url = HTTP_URL + ":" + str(HTTP_PORT)
    api_key = None

    _http_ok_response = 200
    _format_binary = "bin"
    _time_series_request = "time-series"
    _time_series_metadata_request = "time-series-metadata"
    _collection_request = "collection"
    _collection_metadata_request = "collection-metadata"
    _file_store_request = "file-store"
    _file_store_metadata_request = "file-store-metadata"
    _file_metadata_request = "file-metadata"
    _format = "format"
    _type = "type"
    _api_key = 'api_key'
    _test_user_api_key = 'test_user12345'

    @staticmethod
    def setup_jupyter():
        """
        A convenience function that can be used to initialise a Jupyter Notebook (import Python packages, set sensible
        defaults for image sizes etc.) so that it can be used to run any example notebooks provided by the platform.
        """
        # Import the packages typically required

        import geopandas as gpd
        import pandas as pd
        import matplotlib.pyplot as plt

        # Set any defaults typically required

        pd.options.mode.chained_assignment = None
        plt.rcParams["figure.figsize"] = (20, 20)
        Archipelagos.api_key = Archipelagos._test_user_api_key

    @staticmethod
    def build_url(params: Dict[str, str],
                  base_url: str = None,
                  port: int = None) -> str:
        """
        Builds a URL that has parameters, and possibly a port.

        :param params: The parameters to add to the URL.
        :type : Dict[str, str]

        :param base_url: The base URL.
        :type base_url: str

        :param port: The optional port number.
        :type port: int

        :return: The URL.
        :rtype: str
        """
        if base_url is None:
            base_url = Archipelagos._http_url

        if isinstance(port, int):
            base_url = "{0}:{1}".format(base_url, port)

        query_params = {HttpConstants.CLIENT_TYPE_PARAMETER: ClientType.PYTHON_CLIENT}

        for param in params:
            value = params[param]
            if value is None:
                params[param] = ""
            query_params[param] = value

        url_parts = list(urlparse(base_url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(query_params)
        url_parts[4] = urlencode(query)

        return urlunparse(url_parts)

    @staticmethod
    def _get_url_params(url: str) -> Dict[str, str]:
        """
        Obtains the parameters from a URL.

        :param url: The URL.
        :type url: str

        :return: The parameters in url.
        :rtype: dict
        """
        url_parts = list(urlparse(url))
        return dict(parse_qsl(url_parts[4]))

    @staticmethod
    def _update_url_params(url: str,
                           parameters: Dict) -> str:
        """
        Obtains the parameters from a URL.

        :param url: The URL.
        :type url: str

        :param parameters: The parameters to set for the URL.
        :type parameters: Dict

        :return: The update URL.
        :rtype: str
        """
        url_parts = list(urlparse(url))
        url_parts[4] = urlencode(parameters)
        return urlunparse(url_parts)

    @staticmethod
    def send(request) -> Any:
        """
        Send a request to the platform.

        :param request: The request to send to the platform.
        :type request: Any

        :return: The data returned by the platform in a format appropriate to the type of request provided.
        :rtype: Any
        """
        # Obtain the URL and port to use when connecting to the platform

        if Archipelagos._http_url is None:
            raise ValueError("No value has been provided for \"Archipelagos.http_url\"")

        # Check what type of request has been provided

        if isinstance(request, TimeSeriesRequest):
            # Check that an API Key has been provided

            if request.api_key is None:
                api_key = Archipelagos.api_key

                if api_key is None:
                    raise ValueError("Neither the request or Archipelagos contains an API Key")
                else:
                    request.api_key = api_key

            # Build the URL to use in the request

            params = {Archipelagos._format: Archipelagos._format_binary,
                      Archipelagos._type: Archipelagos._time_series_request}
            url = Archipelagos.build_url(params)

            # Build the HTTP request and send to the server

            payload = request.serialize()
            response = requests.post(url, data=payload)

            # Inspect the response

            if response.status_code == Archipelagos._http_ok_response:
                serialized = response.content

                if serialized is None or len(serialized) == 0:
                    raise ValueError("The platform returned a HTTP response but this did contain the expected data")
                else:
                    return TimeSeriesResponse.deserialize(serialized)
            else:
                message = "The platform returned an unexpected HTTP response code ({}) and reason: \"{}}\";"
                message += " response received was:\n\n{}}"
                raise ValueError(message.format(response.status_code, response.reason, response))

        elif isinstance(request, TimeSeriesMetadataRequest):
            # Check that an API Key has been provided

            if request.api_key is None:
                api_key = Archipelagos.api_key

                if api_key is None:
                    raise ValueError("Neither the request or Archipelagos contains an API Key")
                else:
                    request.api_key = api_key

            # Build the URL to use in the request

            params = {Archipelagos._format: Archipelagos._format_binary,
                      Archipelagos._type: Archipelagos._time_series_metadata_request}
            url = Archipelagos.build_url(params)

            # Build the HTTP request and send to the server

            payload = request.serialize()
            response = requests.post(url, data=payload)

            # Inspect the response

            if response.status_code == Archipelagos._http_ok_response:
                serialized = response.content

                if serialized is None or len(serialized) == 0:
                    raise ValueError("The platform returned a HTTP response but this did contain the expected data")
                else:
                    return TimeSeriesMetadataResponse.deserialize(serialized)
            else:
                message = "The platform returned an unexpected HTTP response code ({}) and reason: \"{}}\";"
                message += " response received was:\n\n{}}"
                raise ValueError(message.format(response.status_code, response.reason, response))

        elif isinstance(request, CollectionRequest):
            # Check that an API Key has been provided

            if request.api_key is None:
                api_key = Archipelagos.api_key

                if api_key is None:
                    raise ValueError("Neither the request or Archipelagos contains an API Key")
                else:
                    request.api_key = api_key

            # Build the URL to use in the request

            params = {Archipelagos._format: Archipelagos._format_binary,
                      Archipelagos._type: Archipelagos._collection_request}
            url = Archipelagos.build_url(params)

            # Build the HTTP request and send to the server

            payload = request.serialize()
            response = requests.post(url, data=payload)

            # Inspect the response

            if response.status_code == Archipelagos._http_ok_response:
                serialized = response.content

                if serialized is None or len(serialized) == 0:
                    raise ValueError("The platform returned a HTTP response but this did contain the expected data")
                else:
                    return CollectionResponse.deserialize(serialized)
            else:
                message = "The platform returned an unexpected HTTP response code ({}) and reason: \"{}}\";"
                message += " response received was:\n\n{}}"
                raise ValueError(message.format(response.status_code, response.reason, response))

        elif isinstance(request, CollectionMetadataRequest):
            # Check that an API Key has been provided

            if request.api_key is None:
                api_key = Archipelagos.api_key

                if api_key is None:
                    raise ValueError("Neither the request or Archipelagos contains an API Key")
                else:
                    request.api_key = api_key

            # Build the URL to use in the request

            params = {Archipelagos._format: Archipelagos._format_binary,
                      Archipelagos._type: Archipelagos._collection_metadata_request}
            url = Archipelagos.build_url(params)

            # Build the HTTP request and send to the server

            payload = request.serialize()
            response = requests.post(url, data=payload)

            # Inspect the response

            if response.status_code == Archipelagos._http_ok_response:
                serialized = response.content

                if serialized is None or len(serialized) == 0:
                    raise ValueError("The platform returned a HTTP response but this did contain the expected data")
                else:
                    return CollectionMetadataResponse.deserialize(serialized)
            else:
                message = "The platform returned an unexpected HTTP response code ({}) and reason: \"{}}\";"
                message += " response received was:\n\n{}}"
                raise ValueError(message.format(response.status_code, response.reason, response))

        elif isinstance(request, FileStoreMetadataRequest):
            # Check that an API Key has been provided

            if request.api_key is None:
                api_key = Archipelagos.api_key

                if api_key is None:
                    raise ValueError("Neither the request or Archipelagos contains an API Key")
                else:
                    request.api_key = api_key

            # Build the URL to use in the request

            params = {Archipelagos._format: Archipelagos._format_binary,
                      Archipelagos._type: Archipelagos._file_store_metadata_request}
            url = Archipelagos.build_url(params)

            # Build the HTTP request and send to the server

            payload = request.serialize()
            response = requests.post(url, data=payload)

            # Inspect the response

            if response.status_code == Archipelagos._http_ok_response:
                serialized = response.content

                if serialized is None or len(serialized) == 0:
                    raise ValueError("The platform returned a HTTP response but this did contain the expected data")
                else:
                    return FileStoreMetadataResponse.deserialize(serialized)
            else:
                message = "The platform returned an unexpected HTTP response code ({}) and reason: \"{}}\";"
                message += " response received was:\n\n{}}"
                raise ValueError(message.format(response.status_code, response.reason, response))

        elif isinstance(request, FileStoreRequest):
            # Check that an API Key has been provided

            if request.api_key is None:
                api_key = Archipelagos.api_key

                if api_key is None:
                    raise ValueError("Neither the request or Archipelagos contains an API Key")
                else:
                    request.api_key = api_key

            # Build the URL to use in the request

            params = {Archipelagos._format: Archipelagos._format_binary,
                      Archipelagos._type: Archipelagos._file_store_request}
            url = Archipelagos.build_url(params)

            # Build the HTTP request and send to the server

            payload = request.serialize()
            response = requests.post(url, data=payload)

            # Inspect the response

            if response.status_code == Archipelagos._http_ok_response:
                serialized = response.content

                if serialized is None or len(serialized) == 0:
                    raise ValueError("The platform returned a HTTP response but this did contain the expected data")
                else:
                    return FileStoreResponse.deserialize(serialized)
            else:
                message = "The platform returned an unexpected HTTP response code ({}) and reason: \"{}}\";"
                message += " response received was:\n\n{}}"
                raise ValueError(message.format(response.status_code, response.reason, response))

        elif isinstance(request, FileMetadataRequest):
            # Check that an API Key has been provided

            if request.api_key is None:
                api_key = Archipelagos.api_key

                if api_key is None:
                    raise ValueError("Neither the request or Archipelagos contains an API Key")
                else:
                    request.api_key = api_key

            # Build the URL to use in the request

            params = {Archipelagos._format: Archipelagos._format_binary,
                      Archipelagos._type: Archipelagos._file_metadata_request}
            url = Archipelagos.build_url(params)

            # Build the HTTP request and send to the server

            payload = request.serialize()
            response = requests.post(url, data=payload)

            # Inspect the response

            if response.status_code == Archipelagos._http_ok_response:
                serialized = response.content

                if serialized is None:
                    raise ValueError("The platform returned a HTTP response but this did contain the expected data")
                else:
                    return FileMetadataResponse.deserialize(serialized)
            else:
                message = "The platform returned an unexpected HTTP response code ({}) and reason: \"{}}\";"
                message += " response received was:\n\n{}}"
                raise ValueError(message.format(response.status_code, response.reason, response))

        elif isinstance(request, str):
            # Check that an API Key has been provided

            parameters = Archipelagos._get_url_params(request)
            api_key = parameters[Archipelagos._api_key] if Archipelagos._api_key in parameters else None

            if api_key is None:
                api_key = Archipelagos.api_key

                if api_key is None:
                    raise ValueError("Neither the request or Archipelagos contains an API Key")
                else:
                    parameters[Archipelagos._api_key] = api_key
                    request = Archipelagos._update_url_params(request, parameters)

            # Send the request to the platform and inspect the response

            response = requests.post(request)

            if response.status_code == Archipelagos._http_ok_response:
                serialized = response.content

                if serialized is None or len(serialized) == 0:
                    raise ValueError("The platform returned a HTTP response but this did contain the expected data")
                else:
                    return serialized.decode("utf-8")
            else:
                message = "The platform returned an unexpected HTTP response code ({}) and reason: \"{}}\";"
                message += " response received was:\n\n{}}"
                raise ValueError(message.format(response.status_code, response.reason, response))

        else:
            raise ValueError("An unrecognised type of request has been specified")

    @staticmethod
    def _get_pandas_data_frame(response: Any) -> pd.DataFrame:
        """
        Builds a Pandas Data Frame from a response.

        :param response: The response received by the platform.
        :type response: Any

        :return: The data in response as a Pandas Data Frame.
        :rtype: pd.DataFrame
        """
        if isinstance(response, TimeSeriesResponse):
            if response.error_occurred:
                raise PlatformError(response.error_code, response.error_message)
            else:
                # Process the data in the response object

                features = response.data.metadata.features
                data = {}

                for date_time, feature_map_list in response.data.data.data:
                    if len(feature_map_list) > 1:
                        raise ValueError(
                            'There is more than one set of features for the date/time {}'.format(date_time))

                    elif len(feature_map_list) == 1:
                        feature_values = [None] * len(features)
                        feature_map = feature_map_list[0]

                        for i, feature_value in enumerate(features):
                            feature_values[i] = feature_map.get(feature_value, None)

                        if date_time in data:
                            raise ValueError(
                                'There is more than one set of features for the date/time {}'.format(date_time))
                        else:
                            data[date_time] = feature_values
                    else:
                        data[date_time] = {}

                return pd.DataFrame.from_dict(data, orient='index', columns=features)

        elif isinstance(response, CollectionResponse):
            if response.error_occurred:
                raise PlatformError(response.error_code, response.error_message)
            else:
                # Process the data in the response object

                features = response.data.metadata.features
                data = {}

                for object_id in response.data.data.data:
                    feature_map = response.data.data.data[object_id]
                    feature_values = [None] * len(features)

                    for i, feature_value in enumerate(features):
                        feature_values[i] = feature_map.get(feature_value, None)

                    if object_id in data:
                        raise ValueError(
                            'There is more than one set of features for the ID {}'.format(object_id))
                    else:
                        data[object_id] = feature_values

                return pd.DataFrame.from_dict(data, orient='index', columns=features)

        elif isinstance(response, FileStoreResponse):
            if response.error_occurred:
                raise PlatformError(response.error_code, response.error_message)
            else:
                bytes_io = io.BytesIO(response.file)
                file_name = response.metadata.name.lower()

                if file_name.endswith(".csv"):
                    return pd.read_csv(bytes_io)
                elif file_name.endswith(".json"):
                    return pd.read_json(bytes_io)
                elif file_name.endswith(".xls") or file_name.endswith(".xlsx"):
                    return pd.read_excel(bytes_io)
                else:
                    return pd.read_table(bytes_io)
        else:
            raise ValueError('response is of an unsupported type')

    @staticmethod
    def _get_numpy_array(response: Any) -> np.ndarray:
        """
        Builds a Numpy array from a response.

        :param response: The response received by the platform.
        :type response: Any

        :return: The data in response as a Numpy array.
        :rtype: np.ndarray or None
        """
        if isinstance(response, TimeSeriesResponse):
            if response.error_occurred:
                raise PlatformError(response.error_code, response.error_message)

            else:
                # Initialise the array to return

                features = response.data.metadata.features
                num_cols = len(features) + 1

                data = response.data.data.data
                num_rows = np.sum([len(tup[1]) for tup in response.data.data.data])

                if num_rows > 0:
                    numpy_array = np.empty((num_rows, num_cols), dtype=object)
                    numpy_array[:] = None

                    # Process the data in the response object

                    row_num = 0

                    for date_time, feature_map_list in data:
                        if len(feature_map_list) > 0:
                            for feature_map in feature_map_list:
                                numpy_array[row_num, 0] = date_time

                                for col_num, feature_value in enumerate(features):
                                    numpy_array[row_num, col_num + 1] = feature_map.get(feature_value, None)

                                row_num = row_num + 1
                        else:
                            numpy_array[row_num, 0] = date_time
                            row_num = row_num + 1

                    return numpy_array
                else:
                    return np.empty((0, num_cols))

        elif isinstance(response, CollectionResponse):
            if response.error_occurred:
                raise PlatformError(response.error_code, response.error_message)

            else:
                # Initialise the array to return

                features = response.data.metadata.features
                num_cols = len(features) + 1

                data = response.data.data.data
                num_rows = len(response.data.data.data)

                numpy_array = np.empty((num_rows, num_cols), dtype=object)
                numpy_array[:] = None

                # Process the data in the response object

                row_num = 0

                for object_id in data:
                    feature_map = data[object_id]
                    numpy_array[row_num, 0] = object_id

                    for col_num, feature_value in enumerate(features):
                        numpy_array[row_num, col_num + 1] = feature_map.get(feature_value, None)

                    row_num = row_num + 1

                return numpy_array

        else:
            raise ValueError('response is of an unsupported type')

    @staticmethod
    def _get_geopandas_data_frame(response: Any):
        """
        Builds a GeoPandas Data Frame from a response.

        :param response: The response received by the platform.
        :type response: Any

        :return: The data in response as a GeoPandas Data Frame.
        :rtype: gpd.GeoDataFrame
        """
        if isinstance(response, FileStoreResponse):
            if response.error_occurred:
                raise PlatformError(response.error_code, response.error_message)
            else:
                import geopandas as gpd
                file_name = response.metadata.name.lower()

                if file_name.endswith(".json") or file_name.endswith(".geojson"):
                    bytes_io = io.BytesIO(response.file)
                    file = io.TextIOWrapper(bytes_io, encoding='utf-8')
                    return gpd.read_file(file)

                else:
                    return gpd.read_file(io.BytesIO(response.file))
        else:
            raise ValueError('response is of an unsupported type')

    @staticmethod
    def get_time_series(source: str,
                        code: str, ts_id: str,
                        start: Timestamp = None,
                        end: Timestamp = None,
                        features: List[str] = None,
                        max_size: int = -1,
                        ascending: bool = True,
                        returns: str = "pandas",
                        api_key: str = None) -> pd.DataFrame or np.ndarray or None:
        """
        Retrieve time-series data and (where possible) return it as a specified Python object types; Pandas Data Frames
        and Numpy arrays are currently supported.

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

        :param returns: The object to be returned; "pandas" for a Pandas Data Frame or "numpy" for a Numpy array.
        :type returns: str

        :param api_key: The (optional) API Key.
        :type api_key: str

        :return: The type of object requested.
        :rtype: pd.DataFrame or np.ndarray or None
        """
        if isinstance(returns, str):
            # See what type of object the caller wants

            returns = returns.lower()
            return_pandas = "pandas" == returns or "pd" == returns
            return_numpy = "numpy" == returns or "np" == returns

            if return_pandas or return_numpy:
                # Send the time-series request to the platform

                request = TimeSeriesRequest(source, code, ts_id, start, end, features, max_size, ascending, api_key)
                response = Archipelagos.send(request)

                # Inspect the result and return the appropriate type of object

                if return_pandas:
                    return Archipelagos._get_pandas_data_frame(response)
                elif return_numpy:
                    return Archipelagos._get_numpy_array(response)
                else:
                    return None
            else:
                raise ValueError("The value for the returns parameter \"{}\" is unrecognised".format(returns))
        else:
            raise ValueError("The returns parameter is not of type str")

    @staticmethod
    def get_collection(source: str,
                       code: str,
                       cid: str,
                       features: List[str] = None,
                       max_size: int = -1,
                       returns: str = "pandas",
                       api_key: str = None) -> pd.DataFrame or np.ndarray or None:
        """
        Retrieve collection data and (where possible) return it as a specified Python object types; Pandas Data Frames
        and Numpy arrays are currently supported.

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

        :param returns: The object to be returned; "pandas" for a Pandas Data Frame or "numpy" for a Numpy array.
        :type returns: str

        :param api_key: The (optional) API Key.
        :type api_key: str

        :return: The type of object requested.
        :rtype: pd.DataFrame or np.ndarray or None
        """
        if isinstance(returns, str):
            # See what type of object the caller wants

            returns = returns.lower()
            return_pandas = "pandas" == returns or "pd" == returns
            return_numpy = "numpy" == returns or "np" == returns

            if return_pandas or return_numpy:
                # Send the request to the platform

                request = CollectionRequest(source, code, cid, features, max_size, api_key)
                response = Archipelagos.send(request)

                # Inspect the result and return the appropriate type of object

                if return_pandas:
                    return Archipelagos._get_pandas_data_frame(response)

                elif return_numpy:
                    return Archipelagos._get_numpy_array(response)

                else:
                    return None
            else:
                raise ValueError("The value for the returns parameter \"{}\" is unrecognised".format(returns))
        else:
            raise ValueError("The returns parameter is not of type str")

    @staticmethod
    def get_file(source: str,
                 code: str,
                 fs_id: str,
                 name: str,
                 returns: str = "pandas",
                 api_key: str = None):
        """
        Retrieve collection data and (where possible) return it as a specified Python object types; Pandas Data Frames
        and Numpy arrays are currently supported.

        :param source: The source for the file store.
        :type source: str

        :param code: The code for the file store.
        :type code: str

        :param fs_id: The ID for the file store.
        :type fs_id: str

        :param name: The name of the file.
        :type name: str

        :param returns: The type of object that should be returned; "pandas" for a Pandas Data Frame, "geopandas" for a
        GeoPandas Data Frame, or "numpy" for a Numpy array.
        :type returns: str

        :param api_key: The (optional) API Key.
        :type api_key: str

        :return: The type of object requested.
        :rtype: pd.DataFrame or np.ndarray or gpd.GeoDataFrame.
        """
        if isinstance(returns, str):
            # See what type of object the caller wants

            returns = returns.lower()
            return_pandas = "pandas" == returns or "pd" == returns
            return_geo_pandas = "geopandas" == returns or "gpd" == returns
            return_numpy = "numpy" == returns or "np" == returns

            if return_pandas or return_geo_pandas or return_numpy:
                # Send the request to the platform

                request = FileStoreRequest(source, code, fs_id, name, api_key)
                response = Archipelagos.send(request)

                # Inspect the result and return the appropriate type of object

                if return_pandas:
                    return Archipelagos._get_pandas_data_frame(response)
                elif return_geo_pandas:
                    return Archipelagos._get_geopandas_data_frame(response)
                elif return_numpy:
                    return Archipelagos._get_numpy_array(response)
                else:
                    return None
            else:
                raise ValueError("The value for the returns parameter \"{}\" is unrecognised".format(returns))
        else:
            raise ValueError("The returns parameter is not of type str")
