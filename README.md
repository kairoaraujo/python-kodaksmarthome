[![Build Status](https://github.com/kairoaraujo/python-kodaksmarthome/actions/workflows/merge.yml/badge.svg)](https://github.com/kairoaraujo/python-kodaksmarthome/actions/workflows/merge.yml)
[![Documentation Status](https://readthedocs.org/projects/python-kodaksmarthome/badge/?version=latest)](https://python-kodaksmarthome.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/kairoaraujo/python-kodaksmarthome/branch/master/graph/badge.svg)](https://codecov.io/gh/kairoaraujo/python-kodaksmarthome)
[![pypi Downloads](https://img.shields.io/pypi/dm/python-kodaksmarthome)](https://pypistats.org/packages/python-kodaksmarthome)
[![pypi](https://img.shields.io/pypi/v/python-kodaksmarthome.svg)](https://pypi.python.org/pypi/python-kodaksmarthome)
[![pypi](https://img.shields.io/pypi/l/python-kodaksmarthome.svg)](https://pypi.python.org/pypi/python-kodaksmarthome)


# Python Kodak Smart Home


Python Kodak Smart Home is a library written in Python 3 (>=3.7) that works as API for
[Kodak Smart Home Portal](https://kodaksmarthome.com).

This API uses the credentials from Kodak Smart Home Portal to fetch devices
registered and its events to be used as Python Projects.

***This project is not part of Kodak.***

## Installation

``pip install python-kodaksmarthome``


## Usage


### Initializing the connection

```pycon
>>> from kodaksmarthome import KodakSmartHome
>>> my_home = KodakSmartHome('my@email.com', 'my-pass')
>>> my_home.connect()
>>> my_home.is_connected
True
```


### Listing devices, state, model and device id

```pycon
>>> for device in my_home.get_devices:
...   print(f"Device: {device['name']}")
...   print(f"Device ID: {device['device_id']})
...   print(f"Model: {device['model_name']})
...   print(f"Online: {device['is_online']}\n")
...
Device: Playground
Device ID: '000009999999999999999999'
Model: Cherish 525
Online: False

Device: Bedroom
Device ID: '00000222222222222222222'
Model: Cherish 525
Online: True
```


### Listing last device motion events

```pycon
>>> motion_events = my_home.get_motion_events(device_id="00000222222222222222222")
>>> for event in motion_events[:2]:
...    print(f"snapshot: {event['snapshot']}")
...    print(f"video_recorded: {event['data'][0]['file']}")
...    print(f"data: {event['created_date']}\n")

snapshot: http://video_url/00000222222222222222222/SNAPSHOT.jpg
video_recorded: http://video_url/00000222222222222222222/VIDEO000001.flv
date: 2020-01-04T16:11:48.000Z

snapshot: http://video_url/00000222222222222222222/SNAPSHOT
video_recorded: http://video_url/00000222222222222222222/VIDEO000002.flv
date: 2020-01-04T16:08:52.000Z
```


## Documentation


https://python-kodaksmarthome.readthedocs.io









