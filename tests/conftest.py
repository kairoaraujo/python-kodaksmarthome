#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019, 2020 Kairo de Araujo
#
import json
import pytest
from unittest import mock


class MockRequestsResponse:
    def __init__(self, json_data, status_code, headers):
        self._headers = headers
        self.json_data = json_data
        self._status_code = status_code

    def json(self):
        return self.json_data

    @property
    def text(self):
        return json.dumps(self.json_data)

    @property
    def headers(self):
        return self._headers

    @property
    def status_code(self):
        return self._status_code


@pytest.fixture
def requests_session_mock_ok():
    return mock.MagicMock(
        post=mock.MagicMock(return_value=mock.PropertyMock(status_code=200)),
        get=mock.MagicMock(return_value=mock.PropertyMock(status_code=200)),
        options=mock.MagicMock(
            return_value=mock.PropertyMock(status_code=200)
        ),
    )


@pytest.fixture
def requests_session_mock_error():
    return mock.MagicMock(
        post=mock.MagicMock(return_value=mock.PropertyMock(status_code=500)),
        get=mock.MagicMock(return_value=mock.PropertyMock(status_code=500)),
        options=mock.MagicMock(
            return_value=mock.PropertyMock(status_code=500)
        ),
    )
