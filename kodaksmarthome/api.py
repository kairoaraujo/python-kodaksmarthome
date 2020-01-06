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

    def _get_options(self):
        """
        Verify the connection with Kodak Smart Home portal

        :return: boolean result
        :rtype: bool
        """
        options_response = self.http_session.options(
            self.region_url.URL_TOKEN, headers=HTTP_HEADERS_BASIC
        )
        if options_response.status_code != HTTP_CODE.OK:
            raise ConnectionError(
                "HTTP CODE " + str(options_response.status_code)
            )

        return True

    def _get_token(self):
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

        token_response = self.http_session.post(
            self.region_url.URL_TOKEN,
            headers=HTTP_HEADERS_AUTH,
            data=token_payload,
        )

        if token_response.status_code != HTTP_CODE.OK:
            raise ConnectionError(
                "HTTP CODE "
                + str(token_response.status_code)
                + "DETAILS "
                + str(token_response.text)
            )

        token_json = token_response.json()
        self.token_info["access_token"] = token_json["access_token"]
        self.token_info["token_type"] = token_json["token_type"]
        self.token_info["refresh_token"] = token_json["refresh_token"]
        self.token_info["expires_in"] = token_json["expires_in"]
        self.token_info["scope"] = token_json["scope"]
        self.account_info = token_json["account_info"]
        self.web_urls = token_json["web_urls"]
        self.token_info["access_token"] = token_json["access_token"]
        self.token = self.token_info["access_token"]

        return True

    def _authentication(self):
        """
        Perform authentication to Kodak Smart Home Portal

        :return: True or Raises ``ConnectionError``
        :rtype: bool
        """
        auth_payload = f"username=&password={self.token}&rememberme=false"
        auth_response = self.http_session.post(
            self.region_url.URL_AUTH,
            headers=HTTP_HEADERS_AUTH,
            data=auth_payload,
        )

        if auth_response.status_code != HTTP_CODE.OK:
            raise ConnectionError(
                "HTTP CODE "
                + str(auth_response.status_code)
                + "DETAILS "
                + str(auth_response.text)
            )

        auth_json = auth_response.json()
        self.cookie = self.http_session.cookies["JSESSIONID"]
        self.user_id = auth_json["data"]["id"]

        return True

    def _devices(self):
        """
        Get all devices available in Kodak Smart Home Portal

        :return: all devices
        :rtype: list
        """
        parameters = {"access_token": f"{self.token}"}
        devices_response = self.http_session.get(
            self.region_url.URL_DEVICES,
            headers=HTTP_HEADERS_BASIC,
            params=parameters,
        )
        if devices_response.status_code != HTTP_CODE.OK:
            raise ConnectionError(
                "HTTP CODE "
                + str(devices_response.status_code)
                + "DETAILS "
                + str(devices_response.text)
            )

        devices_json = devices_response.json()
        self.devices = devices_json["data"]

        return self.devices

    def _get_events(self):
        """
        Get all event for all available devices in Kodak Smart Home Portal

        :return: all events
        :rtype: list
        """
        for device in self.devices:
            device_id = device['device_id']
            device_events = {
                'device_id': device_id,
                'events': list()
            }
            pages = 1
            events_pages = 1
            while pages <= events_pages:
                url_events = (
                    f"{self.region_url.URL}/user/device/event?"
                    + f"access_token={self.token}&"
                    + f"device_id={device_id}&"
                    + f"page={pages}"
                )

                events_response = self.http_session.get(
                    url_events, headers=HTTP_HEADERS_BASIC
                )

                if events_response.status_code != HTTP_CODE.OK:
                    raise ConnectionError(
                        "HTTP CODE "
                        + str(events_response.status_code)
                        + "DETAILS "
                        + str(events_response.text)
                    )

                events_json = events_response.json()
                events_pages = events_json["data"]["total_pages"]
                if events_json["data"]["total_events"] == 0:
                    continue
                events = events_json["data"]["events"]
                for event in events:
                    if event not in device_events['events']:
                        device_events['events'].append(event)

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
            self._get_options()
            self._get_token()
            self._authentication()
            self._devices()
            self._get_events()
            self.is_connected = True

        except requests.exceptions.ConnectionError as err:
            raise ConnectionError(str(err))

    def disconnect(self):
        """
        Disconnect from Kodak Smart Portal

        :return: None
        :exception: ``ConnectionError``
        """
        self.http_session.get(self.region_url.URL_LOGOUT)
        self.http_session.close()
        self.is_connected = False

    @property
    def list_devices(self):
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
            ``KodakSmartHome.list_devices``
        :type device_id: str
        :return: list events
        :rtype: list
        """
        if device_id is None:
            return self.events

        else:
            if device_id in [d['device_id'] for d in self.devices]:
                device_events = list(
                    filter(lambda d: d["device_id"] == device_id, self.events)
                )

                return device_events[0]

            else:

                return None

    def _filter_event_type(
        self, device_id=None, event_type=DEVICE_EVENT_MOTION
    ):
        """
        Filter events from device by event type.

        :param device_id: device id available in the device information
            ``KodakSmartHome.list_devices``
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
                        lambda e: e["event_type"] == event_type,
                        device_events["events"],
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

            return sorted(events, key=lambda e: e['created_date'])

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

            return sorted(events, key=lambda e: e['created_date'])

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

            return sorted(events, key=lambda e: e['created_date'])

        else:
            raise ConnectionError(
                f"Kodak Smarthome API is {self.is_connected}"
            )
