#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019, Kairo de Araujo
#

auth_response = {
    "status": 200,
    "msg": "Success",
    "data": {
        "id": 7777,
        "email": "my@email.com",
        "phone_number": None,
        "user_name": "nickname",
        "first_name": "Name",
        "last_name": "Lastname",
        "status": 1,
        "policy_agreed": None,
        "send_limit_upload_enable": True,
        "date_created": "2019-07-05T14:15:53Z",
        "last_updated": "2019-12-17T19:49:06Z",
        "last_sign_in": "2019-12-17T19:49:06Z",
        "last_sign_in_count": None,
        "tandc_id": 4,
        "current_tandc_id": 4,
        "is_marketing_accepted": True,
    },
}

devices_response = {
    "status": 200,
    "msg": "Success",
    "data": {
        "payment_source": 1,
        "plan_id": "plan_01",
        "next_plan_id": None,
        "plan_status": 1,
        "plan_expiry_date": None,
        "plan_next_bill_date": None,
        "web_sub_url": "https://app-eu.kodaksmarthome.com/web#...",
        "web_conn_sub_url": "https://app-eu.kodaksmarthome.com/web#/...",
        "devices": [
            {
                "id": 1000,
                "device_id": "FAKEDEVICEID",
                "plan_id": "plan_01",
                "web_conn_sub_url_by_device": "https://app-eu.kodaksmarth...",
            }
        ],
    },
}

events_response = {
    "status": 200,
    "msg": "Success",
    "total_pages": 1,
    "data": {
        "total_events": 6,
        "total_pages": 1,
        "events": [
            {
                "id": "13889a30-227c-11ea-8790-3fdecad07f1c",
                "event_type": 7,
                "created_date": "2019-12-19T16:24:48.000Z",
                "data": [],
                "dv_data": None,
            },
            {
                "id": "45d55ee0-2279-11ea-8790-3fdecad07f1c",
                "event_type": 7,
                "created_date": "2019-12-19T16:04:44.000Z",
                "data": [],
                "dv_data": None,
            },
            {
                "id": "1095e3e0-2278-11ea-8790-3fdecad07f1c",
                "event_type": 1,
                "created_date": "2019-12-19T15:56:05.000Z",
                "snapshot": "http://snapshot_url",
                "data": [
                    {
                        "file": "http://file_type2_url",
                        "file_type": 2,
                        "storage_id": 2,
                        "id": "3525c8b1-2278-11ea-8790-3fdecad07f1c",
                        "created_date": "2019-12-19T15:57:07.000Z",
                        "file_size": 2574730,
                    },
                    {
                        "file": "http://file_type1_url",
                        "file_type": 1,
                        "storage_id": 2,
                        "id": "154ab961-2278-11ea-8790-3fdecad07f1c",
                        "created_date": "2019-12-19T15:56:13.000Z",
                        "file_size": 308288,
                    },
                ],
                "dv_data": None,
            },
            {
                "id": "ddaac3b0-2277-11ea-8790-3fdecad07f1c",
                "event_type": 7,
                "created_date": "2019-12-19T15:54:40.000Z",
                "data": [],
                "dv_data": None,
            },
            {
                "id": "ab7c3cc0-2277-11ea-8790-3fdecad07f1c",
                "event_type": 1,
                "created_date": "2019-12-19T15:53:16.000Z",
                "snapshot": "http://snapshot_url",
                "data": [
                    {
                        "file": "http://file_type2_url",
                        "file_type": 2,
                        "storage_id": 2,
                        "id": "c6b08051-2277-11ea-8790-3fdecad07f1c",
                        "created_date": "2019-12-19T15:54:01.000Z",
                        "file_size": 1152934,
                    },
                    {
                        "file": "http://file_type1_url",
                        "file_type": 1,
                        "storage_id": 2,
                        "id": "ae4b8961-2277-11ea-8790-3fdecad07f1c",
                        "created_date": "2019-12-19T15:53:20.000Z",
                        "file_size": 71552,
                    },
                ],
                "dv_data": None,
            },
            {
                "id": "c71516a0-2f3d-11ea-8790-3fdecad07f1c",
                "event_type": 2,
                "created_date": "2020-01-04T22:01:36.000Z",
                "data": [],
                "dv_data": None,
            },
        ],
    },
}
