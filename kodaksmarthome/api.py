#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Kairo de Araujo
#
import requests

from kodaksmarthome.constants import (
    HTTP_HEADERS_AUTH,
    HTTP_HEADERS_BASIC,
    HTTP_CODE,
    HTTP_CLIENT_MODEL,
    DEVICE_EVENT_BATTERY,
    DEVICE_EVENT_SOUND,
    DEVICE_EVENT_MOTION,
    SUPPORTED_REGIONS,
    _URLS,
)


class KodakSmartHome:
    """Kodak Smart Home API session.

    Provides connection to Kodak Smart Home portal.

    :param username: username registered in Kodak Smart Home Portal
    :type username: str
    :param password: password registered in Kodak Smart Home Portal
    :type password: str
    :param region: Global Region Portal. Options: 'EU'. Default: 'EU'
    :type region: str
    """

    def __init__(self, username, password, region="EU"):

        self.username = username
        self.password = password
        self.http_session = requests.Session()
        self.token = None
        self.account_info = None
        self.web_urls = None
        self.devices = list()
        self.events = list()
        self.is_connected = False

        if region not in SUPPORTED_REGIONS:
            raise AttributeError(f"{region} is not supported")

        else:
            self.region_url = _URLS(SUPPORTED_REGIONS[region])

    def _http_request(self, method, url, headers=None, data=None, params=None):

        try:
            if method == "POST":
                http_response = self.http_session.post(
                    url, headers=headers, data=data, params=params
                )

            elif method == "OPTIONS":
                http_response = self.http_session.options(
                    url, headers=headers, data=data, params=params
                )

            elif method == "GET":
                http_response = self.http_session.get(
                    url, headers=headers, data=data, params=params
                )

            else:
                raise AttributeError(f"Invalid Method {method}")

        except requests.exceptions.ConnectionError as err:
            raise ConnectionError(str(err))

        status_code = http_response.status_code
        content_type = None
        response_json = None
        response_text = http_response.text
        error = None
        error_description = None

        if "Content-Type" in http_response.headers:
            content_type = http_response.headers["Content-Type"]

        if content_type and "application/json" in content_type:
            response_json = http_response.json()

            if "error" in response_json:
                error = response_json["error"]

            if "error_description" in response_json:
                error_description = response_json["error_description"]

        if status_code == HTTP_CODE.OK:
            if response_json:
                self.is_connected = True
                return response_json

            elif response_json is None and method == "OPTIONS":
                return True

            else:
                self.is_connected = False
                raise TypeError("Unexpected response format")

        elif status_code == HTTP_CODE.UNAUTHORIZED:
            if error == "invalid_grant":
                self.is_connected = False

                raise ConnectionError(error_description)

            elif (
                type(error) == dict
                and "reason" in error
                and error["reason"] == "authError"
                and self.is_connected
            ):
                self.is_connected = False
                return True

            elif (
                type(error) == dict
                and "reason" in error
                and error["reason"] == "authError"
                and self.is_connected is False
            ):
                if "message" in error:
                    raise ConnectionError(error["message"])

            elif (
                "msg" in response_json
                and "Access Denied" in response_json["msg"]
                and self.is_connected
            ):
                self.is_connected = False
                return True

            elif (
                "msg" in response_json
                and "Access Denied" in response_json["msg"]
                and self.is_connected is False
            ):
                self.is_connected = False
                raise ConnectionError(response_json["msg"])

            else:
                self.is_connected = False

                raise ConnectionError("Unexpected 401 error " + response_text)

        else:
            self.is_connected = False
            raise ConnectionError(
                "Unexpected HTTP CODE error " + response_text
            )

    def _options(self):
        """
        Verify the connection with Kodak Smart Home portal

        :return: boolean result
        :rtype: bool
        """
        options_response = self._http_request(
            "OPTIONS", self.region_url.URL_TOKEN, headers=HTTP_HEADERS_BASIC
        )

        return options_response

    def _token(self):
        """
        Get Kodak Smart Home Portal Token

        :return: True or Raises ``ConnectionError``
        :rtype: bool
        :exception: ``ConnectionError``
        """
        self.token_info = {
            "access_token": None,
            "token_type": None,
            "refresh_token": None,
            "expires_in": None,
            "scope": None,
        }

        token_payload = (
            "grant_type=password&"
            + f"username={self.username}&"
            + f"password={self.password}&"
            + f"model={HTTP_CLIENT_MODEL}"
        )

        token_response = self._http_request(
            "POST",
            self.region_url.URL_TOKEN,
            headers=HTTP_HEADERS_AUTH,
            data=token_payload,
        )

        self.token_info["access_token"] = token_response["access_token"]
        self.token_info["token_type"] = token_response["token_type"]
        self.token_info["refresh_token"] = token_response["refresh_token"]
        self.token_info["expires_in"] = token_response["expires_in"]
        self.token_info["scope"] = token_response["scope"]
        self.account_info = token_response["account_info"]
        self.web_urls = token_response["web_urls"]
        self.token_info["access_token"] = token_response["access_token"]
        self.token = self.token_info["access_token"]

        return True

    def _authentication(self):
        """
        Perform authentication to Kodak Smart Home Portal

        :return: True or Raises ``ConnectionError``
        :rtype: bool
        """
        auth_payload = f"username=&password={self.token}&rememberme=false"
        auth_response = self._http_request(
            "POST",
            self.region_url.URL_AUTH,
            headers=HTTP_HEADERS_AUTH,
            data=auth_payload,
        )

        self.cookie = self.http_session.cookies["JSESSIONID"]
        self.user_id = auth_response["data"]["id"]

        return True

    def _get_devices(self):
        """
        Get all devices available in Kodak Smart Home Portal

        :return: all devices
        :rtype: list
        """

        headers = HTTP_HEADERS_BASIC
        headers["Authorization"] = f"Bearer {self.token}"

        devices_response = self._http_request(
            "GET",
            self.region_url.URL_DEVICES,
            headers=headers,
        )

        if self.is_connected is False:
            self.connect()

            return self.devices

        else:
            self.devices = devices_response["data"]

        return self.devices

    def _get_events(self):
        """
        Get all event for all available devices in Kodak Smart Home Portal

        :return: all events
        :rtype: list
        """

        headers = HTTP_HEADERS_BASIC
        headers["Authorization"] = f"Bearer {self.token}"

        self.events = list()
        for device in self.devices:
            device_id = device["device_id"]
            device_events = {"device_id": device_id, "events": list()}
            pages = 1
            events_pages = 1
            while pages <= events_pages:
                url_events = (
                    f"{self.region_url.URL}/user/device/event?"
                    + f"deviceId={device_id}&"
                    + f"page={pages}"
                )

                events_response = self._http_request(
                    "GET", url_events, headers=headers
                )

                if self.is_connected is False:
                    self.connect()
                    break

                events_pages = events_response["data"]["total_pages"]
                if events_response["data"]["total_events"] == 0:
                    continue

                events = events_response["data"]["events"]
                for event in events:
                    if event not in device_events["events"]:
                        device_events["events"].append(event)

                pages += 1

            self.events.append(device_events)

        return self.events

    def connect(self):
        """
        Connect to Kodak Smart Home Portal and get all information needed.

        :return: None
        :exception: ``ConnectionError``
        """
        try:
            self._options()
            self._token()
            self._authentication()
            self._get_devices()
            self._get_events()

        except requests.exceptions.ConnectionError as err:
            raise ConnectionError(str(err))

    def update(self):
        """
        Update the device list and events data

        :return: True
        :rtype: bool
        :exception: ``ConnectionError``
        """
        self._get_devices()
        self._get_events()

    def disconnect(self):
        """
        Disconnect from Kodak Smart Portal

        :return: None
        :exception: ``ConnectionError``
        """
        self._http_request("GET", self.region_url.URL_LOGOUT)
        self.http_session.close()
        self.is_connected = False

    @property
    def get_devices(self):
        """
        List all registered devices in Kodak Smart Portal and its details.

        :return: all devices and information
        :exception: ``ConnectionError``
        :rtype: list
        """
        if self.is_connected:
            return self.devices

        else:
            raise ConnectionError(
                f"Kodak Smarthome API is {self.is_connected}"
            )

    @property
    def get_events(self):
        """
        Get all devices events

        :return: list of devices events
        :exception: ``ConnectionError``
        :rtype: list
        """
        if self.is_connected:
            return self.events

        else:
            raise ConnectionError(
                f"Kodak Smarthome API is {self.is_connected}"
            )

    def get_events_device(self, device_id=None):
        """
        Get all device events

        :param device_id: device id available in the device information
            ``KodakSmartHome.get_devices``
        :type device_id: str
        :return: list events
        :rtype: list
        """
        if device_id is None:
            return self.events

        else:
            if device_id in [d["device_id"] for d in self.devices]:
                device_events = list(
                    filter(lambda d: d["device_id"] == device_id, self.events)
                )

                events = device_events[0]["events"]
                return sorted(events, key=lambda e: e["created_date"])

            else:

                return None

    def _filter_event_type(
        self, device_id=None, event_type=DEVICE_EVENT_MOTION
    ):
        """
        Filter events from device by event type.

        :param device_id: device id available in the device information
            ``KodakSmartHome.get_devices``
        :param event_type: Possible events``kodaksmarthome.constants``:
            DEVICE_EVENT_MOTION, DEVICE_EVENT_SOUND, DEVICE_EVENT_BATTERY.
            Default: DEVICE_EVENT_MOTION
        :return: events type from specified device
        :rtype: list
        """
        if self.is_connected:
            device_events = self.get_events_device(device_id=device_id)

            if device_events is None:
                return None

            if device_id is None:
                motion_events = list()
                for device in device_events:
                    motion_events += list(
                        filter(
                            lambda e: e["event_type"] == event_type,
                            device["events"],
                        )
                    )

            else:
                motion_events = list(
                    filter(
                        lambda e: e["event_type"] == event_type, device_events
                    )
                )

            return motion_events

        else:
            raise ConnectionError(
                f"Kodak Smarthome API is {self.is_connected}"
            )

    def get_motion_events(self, device_id=None):
        """
        List all motion devices events from specific device sorted by
        creation date.

        :return: list of motion devices events
        :exception: ``ConnectionError``
        :rtype: list
        """
        if self.is_connected:
            events = self._filter_event_type(
                device_id=device_id, event_type=DEVICE_EVENT_MOTION
            )

            if events is None:

                return list()

            return sorted(events, key=lambda e: e["created_date"])

        else:
            raise ConnectionError(
                f"Kodak Smarthome API is {self.is_connected}"
            )

    def get_battery_events(self, device_id=None):
        """
        List all battery devices events from specific device, sorted by
        creation date.

        :return: list of battery devices events
        :exception: ``ConnectionError``
        :rtype: list
        """
        if self.is_connected:
            events = self._filter_event_type(
                device_id=device_id, event_type=DEVICE_EVENT_BATTERY
            )

            if events is None:

                return list()

            return sorted(events, key=lambda e: e["created_date"])

        else:
            raise ConnectionError(
                f"Kodak Smarthome API is {self.is_connected}"
            )

    def get_sound_events(self, device_id=None):
        """
        List all sound devices events from specific device sorted by
        creation date.

        :return: list of sound devices events
        :exception: ``ConnectionError``
        :rtype: list
        """
        if self.is_connected:
            events = self._filter_event_type(
                device_id=device_id, event_type=DEVICE_EVENT_SOUND
            )

            if events is None:

                return list()

            return sorted(events, key=lambda e: e["created_date"])

        else:
            raise ConnectionError(
                f"Kodak Smarthome API is {self.is_connected}"
            )
