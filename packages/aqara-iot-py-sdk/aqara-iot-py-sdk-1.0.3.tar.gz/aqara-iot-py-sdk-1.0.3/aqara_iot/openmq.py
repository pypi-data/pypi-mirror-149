"""Aqara Open IOT HUB which base on MQTT."""
from __future__ import annotations
# from multiprocessing import set_forkserver_preload

import time
import threading
import time
from typing import Any, Callable
from typing import Optional
from paho.mqtt import client as mqtt
from .openlogging import logger
from Crypto.Cipher import AES
import base64


# 数据类
class MData():
    def __init__(self, data = b"",characterSet='utf-8'):
        # data肯定为bytes
        self.data = data
        self.characterSet = characterSet

    def from_string(self,data):
        self.data = data.encode(self.characterSet)
        return self.data

    def from_base64(self,data):
        self.data = base64.b64decode(data.encode(self.characterSet))
        return self.data

    def to_string(self):
        return self.data.decode(self.characterSet)

    def to_base64(self):
        return base64.b64encode(self.data).decode()

    def __str__(self):
        try:
            return self.toString()
        except Exception:
            return self.toBase64()


### 封装类
class AEScryptor():
    def __init__(self,key,mode,iv = '',paddingMode= "NoPadding",characterSet ="utf-8"):
        '''
        构建一个AES对象
        key: 秘钥，字节型数据
        mode: 使用模式，只提供两种，AES.MODE_CBC, AES.MODE_ECB
        iv： iv偏移量，字节型数据
        paddingMode: 填充模式，默认为NoPadding, 可选NoPadding，ZeroPadding，PKCS5Padding，PKCS7Padding
        characterSet: 字符集编码
        '''
        self.key = key
        self.mode = mode
        self.iv = iv
        self.characterSet = characterSet
        self.paddingMode = paddingMode
        self.data = ""
        self.aes = AES.new(self.key,self.mode) 
        self.m_data = MData(characterSet=self.characterSet)

    def set_key(self,key):
        self.key = bytes(key, encoding='UTF-8')
        self.aes = AES.new(self.key,self.mode) 

    def __strip_zero_padding(self,data):
        data = data[:-1]
        while len(data) % 16 != 0:
            data = data.rstrip(b'\x00')
            if data[-1] != b"\x00":
                break
        return data

    def __strip_pkcs5_7padding(self,data):
        paddingSize = data[-1]
        return data.rstrip(paddingSize.to_bytes(1,'little'))

    def __strip_padding_data(self,data):
        if self.paddingMode == "NoPadding":
            return self.__strip_zero_padding(data)
        elif self.paddingMode == "ZeroPadding":
            return self.__strip_zero_padding(data)

        elif self.paddingMode == "PKCS5Padding" or self.paddingMode == "PKCS7Padding":
            return self.__strip_pkcs5_7padding(data)
        else:
            print("不支持Padding")
 

    def decrypt_from_bytes(self,entext)->str:
        '''
        从二进制进行AES解密
        entext: 数据类型bytes
        '''
        rawdata = base64.b64decode(entext) 
        data = self.aes.decrypt(rawdata)
        self.m_data.data = self.__strip_padding_data(data)
        return self.m_data.to_string()


class AqaraMQConfig:
    """Aqara mqtt config."""

    def __init__(self, cfg: dict[str, str] = {}) -> None:
        """Init AqaraMQConfig."""
        #  {
        #     "password": "BG2FRrJTIGCaHTP4Ga2Mlfrr",
        #     "clientId": "omqt.9617f124-a3e3-45fb-8cc5-64c2017b99d5",
        #     "subscribeTopic": "receive_omqt.9617f124-a3e3-45fb-8cc5-64c2017b99d5",
        #     "mqttHost": "aiot-mqtt-test.aqara.cn",
        #     "userName": "9478646628902215681ddba4",
        #     "mqttPort": "1883",
        #     "publishTopic": "control_omqt.9617f124-a3e3-45fb-8cc5-64c2017b99d5"
        # }

        self.password = cfg.get("password", "")
        self.client_id = cfg.get("clientId", "")
        self.source_topic = cfg.get("publishTopic", {})
        self.host = cfg.get("mqttHost", "")
        self.port = int(cfg.get("mqttPort", 0))
        self.username = cfg.get("userName", "")
        self.subscribe_topic = cfg.get("subscribeTopic", {})
        self.expire_time = cfg.get("expireTime", 7200)


class AqaraOpenMQ(threading.Thread):
    """Aqara open iot mqtt client.

    eg:
    aqara_mq = AqaraOpenMQ()
    aqara_mq.set_get_config(device_manager.config_mqtt_add)
    aqara_mq.add_message_listener(device_manager.on_message)
    aqara_mq.start()

    """

    def __init__(self, is_debug=False) -> None:
        """Init AqaraOpenMQ."""
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.client = None
        self.need_reconnect = True
        self.mq_config = None
        self.message_listeners = set()
        self.get_config = None
        self.is_debug = is_debug
        key = b"qam5QPjtFEklN9igQqTQh8Of"  #key will update, when _get_mqtt_config() called.
        self.aes  = AEScryptor(key,AES.MODE_ECB,iv=b"0000000000000000",paddingMode= "PKCS5Padding",characterSet='utf-8')

    def set_get_config(self, get_config: Callable[[str], None]):
        """set the callback func which will be used to get mqtt config"""
        self.get_config = get_config

    def _get_mqtt_config(self) -> Optional[AqaraMQConfig]:
        if self.get_config is None:
            return None

        cfg = AqaraMQConfig(self.get_config())

        if cfg.host == "":
            return None
        else:
            self.aes.set_key(cfg.password)
            return cfg

    def _on_disconnect(self, client, userdata, rc):
        logger.debug("disconnect called")        
        if self.client is not None and self.need_reconnect:
            # 每次断开都会更改 client 和 use name password，重连需要重新设置
            try:
                mq_config = self._get_mqtt_config()
                if mq_config is not None:
                    self.client._client_id = mq_config.client_id
                    self.client.username_pw_set(mq_config.username, mq_config.password)
                    self.client.user_data_set({"mqConfig": mq_config})
            except:
                logger.error("_on_disconnect error.")
            


    def _on_connect(self, mqttc: mqtt.Client, user_data: Any, flags, rc):
        logger.debug(f"connect flags->{flags}, rc->{rc}")
        if rc == 0:
            mqttc.subscribe(user_data["mqConfig"].subscribe_topic)

    def _on_message(self, mqttc: mqtt.Client, user_data: Any, msg: mqtt.MQTTMessage):
        logger.debug(f"payload-> {msg.payload}")

        # {
        #     "data":[
        #             {   "resourceId":"14.7.111",
        #                 "time":"1646303154714",
        #              "triggerSource":{"time":"1646303154","type":4},
        #              "value":"1",
        #              "subjectId":"virtual.93083750786711",
        #              "statusCode":0}
        #              ],

        #  "msgId":"AC10C8A4001E18B4AAC20E41363B00371",
        #  "msgType":"resource_report",
        #  "openId":"853851328861948953623941439489",
        #  "time":"1646303154747"
        #  }
		#data = msg.payload.decode("utf8")
        data:str = ""        
        try :
            data = self.aes.decrypt_from_bytes(msg.payload)         # decode 
        except:
            data = msg.payload.decode("utf8")

        for listener in self.message_listeners:
            listener(data)

    def _on_subscribe(self, mqttc: mqtt.Client, user_data: Any, mid, granted_qos):
        logger.debug(f"_on_subscribe: {mid}")

    def _on_log(self, mqttc: mqtt.Client, user_data: Any, level, string):
        logger.debug(f"_on_log: {string}")

    def run(self):
        """Method representing the thread's activity which should not be used directly."""
       
        self.__run_mqtt()

        time.sleep(30)

        while 1==1:
                try:
                    if self.client is None:
                        time.sleep(60)
                        if self.client is None:
                          self.__run_mqtt()
                          continue

                    if self.client._thread._is_stopped:
                        self.client.loop_stop
                        time.sleep(20)
                        self.__run_mqtt()
                    else:
                        time.sleep(20)
                except Exception :
                        time.sleep(60)
           
    def __run_mqtt(self):
        mq_config = self._get_mqtt_config()
        if mq_config is None:
            logger.error("error while get mqtt config")
            time.sleep(60)
            return

        self.mq_config = mq_config

        logger.debug(f"connecting {mq_config.host}")

        if self.client is not None:
            self.need_reconnect = False
            self.client.disconnect()

        mqttc = self._start(mq_config)
        self.client = mqttc
        self.need_reconnect = True

    def _start(self, mq_config: AqaraMQConfig) -> mqtt.Client:
        mqttc = mqtt.Client(mq_config.client_id)
        mqttc.username_pw_set(mq_config.username, mq_config.password)
        mqttc.user_data_set({"mqConfig": mq_config})
        mqttc.on_connect = self._on_connect
        mqttc.on_message = self._on_message
        mqttc.on_subscribe = self._on_subscribe
        # mqttc.on_log = self._on_log
        mqttc.on_disconnect = self._on_disconnect

        # url = urlsplit(mq_config.url)
        # if url.scheme == "ssl":
        #     mqttc.tls_set()

        # mqttc.tls_set()

        mqttc.connect(mq_config.host, mq_config.port)

        mqttc.loop_start()
        return mqttc

    def start(self):
        """Start mqtt.

        Start mqtt thread
        """
        logger.debug("start")
        super().start()

    def stop(self):
        """Stop mqtt.

        Stop mqtt thread
        """
        logger.debug("stop")
        self.need_reconnect = False
        self.message_listeners = set()
        if self.client is not None:
            self.client.disconnect()
            self.client = None
        self._stop_event.set()

    def add_message_listener(self, listener: Callable[[str], None]):
        """Add mqtt message listener."""
        self.message_listeners.add(listener)

    def remove_message_listener(self, listener: Callable[[str], None]):
        """Remvoe mqtt message listener."""
        self.message_listeners.discard(listener)
