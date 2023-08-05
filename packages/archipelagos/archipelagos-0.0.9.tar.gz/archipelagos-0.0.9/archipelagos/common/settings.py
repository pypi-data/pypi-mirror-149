"""
Classes and functions useful when dealing with settings files.
"""
from __future__ import annotations

from typing import Dict, Any, List
import os


class SettingNames:
    """
    A set of constants representing the names of settings.
    """
    # Settings related to the HTTP server

    HTTP_SERVER_URL = "http.server.url"
    HTTP_SERVER_PORT = "http.server.port"


class SettingsFile:
    """
    Deals with finding and parsing settings files.
    """
    def __init__(self,
                 file_path: str):
        """
        :param file_path: The full path of the settings file.
        :type file_path: str
        """
        self._file_path = file_path

        # Read in the file and store its contents

        with open(file_path) as file:
            lines = file.readlines()

        # Parse the contents of the file

        settings = dict()
        line_count = 0

        for line in lines:
            line_count += 1
            line = line.rstrip().lstrip()

            # Check that the line is not empty and is not a comment (which start with #)

            if line and not line.startswith('#'):
                index = line.find("=")

                if index == -1:
                    raise ValueError(f"Line number {line_count} contains a line that is not empty and does not contain a valid setting.")
                else:
                    setting = line[:index]
                    value = line[index + 1:]

                    if setting in settings:
                        raise ValueError(f"Line number {line_count} contains a duplicate setting for \"{setting}\"")
                    else:
                        settings[setting] = value

        self._settings = Settings(self, settings)

    @property
    def file_path(self) -> str:
        """
        The full file path of the settings file.
        """
        return self._file_path

    @property
    def settings(self) -> Settings:
        """
        The settings contained in the settings file.
        """
        return self._settings

    @staticmethod
    def _locate_file(filename: str,
                     file_paths: List[str]) -> str or None:
        """
        Used to locate the settings file in a list of filenames contained within a directory.

        :param filename: The name of the configuration file.
        :type filename: str

        :param file_paths: The paths of the files in the directory.
        :type file_paths: str

        :return: The file path, or None if it could not be found.
        :rtype: str or None
        """
        to_return = None

        for file_path in file_paths:
            if os.path.isfile(file_path):
                head, tail = os.path.split(file_path)
                if filename == tail:
                    to_return = file_path
                    break
            elif os.path.isdir(file_path):
                file_paths_in_directory = [os.path.join(file_path, filename) for filename in os.listdir(file_path)]
                to_return = SettingsFile._locate_file(filename, file_paths_in_directory)

                if to_return is not None:
                    break
            else:
                pass

        return to_return

    @staticmethod
    def locate(filename: str,
               search_directory: str) -> SettingsFile or None:
        """
        Used to locate a settings file.

        :param filename The name of the  file.
        :type filename: str

        :param search_directory The directory in which the search should start.
        :type search_directory: str

        :return The  file or None if it could not be found.
        :rtype: SettingsFile or None
        """
        file_paths_in_search_directory = [os.path.join(search_directory, filename) for filename in os.listdir(search_directory)]
        to_return = None

        if file_paths_in_search_directory:
            configuration_file_path = SettingsFile._locate_file(filename, file_paths_in_search_directory)

            if configuration_file_path is not None:
                try:
                    to_return = SettingsFile(configuration_file_path)
                except:
                    pass

        return to_return


class Settings:
    """
    Represents the settings contained in a settings file.
    """
    def __init__(self,
                 settings_file: SettingsFile,
                 settings: Dict[str, str]):
        """
        :param settings_file: The settings file associated with the settings.
        :type settings_file: SettingsFile

        :param settings: The settings associated with this.
        :type settings: Dict[str, str]
        """
        self._configuration_file = settings_file
        self._settings = settings

    @property
    def settings_file(self) -> SettingsFile:
        """
        The file associated with the settings.
        """
        return self._configuration_file

    @property
    def settings(self) -> Dict[str, str]:
        """
        The settings associated with this.
        """
        return self._settings

    def has_setting(self, setting: str) -> bool:
        """
        Determines if this has a specified setting.

        :param setting: The setting.
        :type setting: bool

        :return: True if this contains a specified setting, False otherwise.
        :rtype: bool
        """
        return setting in self._settings

    def get_setting(self, setting: str) -> Any:
        """
        Returns a specified setting.

        :param setting: The setting.
        :type setting: bool

        :return: If has_setting(setting) the value of the specified setting, None otherwise.
        :rtype: bool
        """
        return self._settings.get(setting, None)
