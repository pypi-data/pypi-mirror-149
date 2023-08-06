# Aqara IoT Python SDK



![PyPI](https://img.shields.io/pypi/v/aqara-iot-py-sdk)

![PyPI - Downloads](https://img.shields.io/pypi/dm/aqara-iot-py-sdk)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aqara-iot-py-sdk)


A Python sdk for Aqara home assistant. 


## Features
### Base APIs
- AqaraOpenAPI
	- connect
	- is_connect
	- get
	- post
	- put
	- delete
 	
- AqaraOpenMQ
	- start
	- stop
	- add_message_listener
	- remove_message_listener

### APIs
- AqaraDeviceListener
	- update_device
	- add_device
	- remove_device

#### Device control
- AqaraDeviceManager
	- generate_devices_and_update_value
	- add_device_listener
	- remove_device_listener
	- remove_device
	- remove_device_list
	- send_commands

#### Home 
- AqaraHomeDeviceManage
	- update_device_cache
	- query_scenes
	- trigger_scene



## Possible scenarios



- [HomeAssistant Aqara Plugin](https://github.com/aqara/aqara-home-assistant)

- [Aqara Connector Python](https://github.com/aqara/aqara-connector-python)

- ...


## Prerequisite

### Registration


## Usage

## Installation

`pip3 install aqara-iot-py-sdk`

## Sample code


## Aqara Open API reference


## Issue feedback


## License

aqara-iot-py-sdk is available under the MIT license. Please see the [LICENSE](./LICENSE) file for more info.
