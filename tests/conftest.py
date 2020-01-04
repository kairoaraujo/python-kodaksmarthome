#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019, 2020 Kairo de Araujo
#
import pytest
from unittest import mock


class MockRequestsResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


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
