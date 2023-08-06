"""Aqara Open API."""
from __future__ import annotations

import hashlib

# import hmac
import json
import time
import random
from typing import Any

import requests

from .openlogging import filter_logger, logger
from .aqara_enums import (
    APPS,
    AQARA_COUNTRIES,
    PATH_ACCESS_TOKEN,
    PATH_AUTH,
    PATH_OPEN_API,
)

AQARA_ERROR_CODE_ACCESSTOKEN_INCORRECT = 2004
AQARA_ERROR_CODE_ACCESSTOKEN_EXPIRED = 2005

# 108	Token has expired	token已过期
# 109	Token is absence	token缺失
# 804	Token failed	token失效
# 2004	AccessToken incorrect	访问令牌错误
# 2005	AccessToken expired	访问令牌过期
# 2006	RefreshToken incorrect	刷新令牌错误
# 2007	RefreshToken expired	刷新令牌过期


class AqaraTokenInfo:
    """Aqara token info."""

    def __init__(self, token_response: dict[str, Any] = None):
        """Init AqaraTokenInfo."""
        self.expire_time = int(token_response.get("expires_in", 0)) + int(time.time())
        self.access_token = token_response.get("access_token", "")
        self.refresh_token = token_response.get("refresh_token", "")
        self.uid = token_response.get("openId", "")


class AqaraOpenAPI:
    """Open Api.
    access_token	String	否	通过授权获取的访问Token
    Appid	String	是	第三方应用的Appid
    Keyid	String	是	appKey对应id
    Nonce	String	是	随机字符串,每次请求都不同
    Time	String	是	请求时间戳,单位毫秒
    Sign	String	是	请求签名
    Lang	Enum	否	语言,默认英文,'zh', 'en'

    Typical usage example:

    openapi = AqaraOpenAPI(country_code)
    """

    def __init__(
        self,
        country_code: str = "",  # endpoint: str,
    ) -> None:
        """Init AqaraOpenAPI."""
        # self.endpoint = endpoint
        self.session = requests.Session()
        self.session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=50, max_retries=3))
        self.session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=50, max_retries=3))
    
        self.__country_code = country_code
        country = [
            country
            for country in AQARA_COUNTRIES
            if country.country_code == self.__country_code
        ]
        if len(country) > 0:
            self.endpoint = country[0].endpoint

        # self.access_token = ""
        self.app_id = APPS.get(country[0].name).APP_ID
        self.key_id = APPS.get(country[0].name).KEY_ID
        self.app_key = APPS.get(country[0].name).APP_KEY
        self.lang = "en"

        self.token_info: AqaraTokenInfo = None
        self.__username = ""
        self.__password = ""
        self.__schema = ""

    # def login(self, username:str, password:str):
    #     self.__username = username
    #     self.__password = password

    def __nonce(self, length=16) -> str:
        """Generate pseudorandom number."""
        return "".join([str(random.randint(0, 9)) for i in range(length)])

    def __timestamp(self):
        """Generate time stamp."""
        return str(int(time.time() * 1000))

    # https://opendoc.aqara.cn/docs/%E4%BA%91%E5%AF%B9%E6%8E%A5%E5%BC%80%E5%8F%91%E6%89%8B%E5%86%8C/API%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97/Sign%E7%94%9F%E6%88%90%E8%A7%84%E5%88%99.html
    def __calculate_sign(self, nonce: str, t: str) -> str:
        """calculate signate."""
        if self.token_info is None:
            head_data = [
                "appid=",
                self.app_id,
                "&Keyid=",
                self.key_id,
                "&nonce=",
                nonce,
                "&time=",
                t,
                self.app_key,
            ]
        else:
            head_data = [
                "accesstoken=",
                self.token_info.access_token,
                "&appid=",
                self.app_id,
                "&Keyid=",
                self.key_id,
                "&nonce=",
                nonce,
                "&time=",
                t,
                self.app_key,
            ]

        header = "".join(head_data).lower()
        # logger.debug(f"time:{t},header:{header}")
        md5 = hashlib.md5()
        md5.update(header.encode("utf-8"))
        md5_str = md5.hexdigest()
        return md5_str

    def __get_code(self, resp) -> int:
        if resp is not None and "code" in resp:
            return resp.get("code", -1)
        return -1

    def __refresh_access_token_if_need(self, intent: str):
        if self.is_connect() is False:
            return

        if (
            intent == "config.auth.getAuthCode"
            or intent == "config.auth.getToken"
            or intent == "config.auth.refreshToken"
        ):
            return

        # should use refresh token?
        now = int(time.time())
        expired_time = self.token_info.expire_time

        if expired_time - 60 > now:  # 1min
            return

        self.token_info.access_token = ""

        body = {
            "intent": "config.auth.refreshToken",
            "data": {"refreshToken": self.token_info.refresh_token},
        }
        resp = self.post(PATH_OPEN_API, body)
        if self.__get_code(resp) == 0:
            self.token_info = AqaraTokenInfo(resp)

    def set_dev_channel(self, dev_channel: str):
        """Set dev channel."""
        self.dev_channel = dev_channel

    def get_auth(
        self,
        username: str = "",
        password: str = "",
        # country_code: str = "",
        schema: str = "",
    ) -> bool:

        self.__username = username
        self.__password = password

        self.__schema = schema
        self.token_info = None

        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        passwd_md5 = md5.hexdigest().lower()
        # params = {"Content-Type": 'application/x-www-form-urlencoded;charset=utf-8'}

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        req_data = {
            "client_id": self.app_id,
            "response_type": "code",
            "redirect_uri": "https://developer.aqara.com/",
            "account": username,
            # "password":password,
            "passwordExt": passwd_md5,
            "state": 0,
        }
    
        resp = self.session.post(self.endpoint + PATH_AUTH, data=req_data, headers=headers)
        # print(resp.text)
        if resp.ok is False:
            return False

        ack_data = resp.json()
        if self.__get_code(ack_data) != 0:
            return False

        auth_code = ack_data.get("result", {}).get("code", "")

        req_data = {
            "client_id": self.app_id,
            "client_secret": self.app_key,
            "redirect_uri": "https://developer.aqara.com/",
            "grant_type": "authorization_code",
            "code": auth_code,
        }

        resp = self.session.post(
            self.endpoint + PATH_ACCESS_TOKEN, data=req_data, headers=headers
        )
        if resp.ok is False:
            return False
        

        ack_data = resp.json()
        if ack_data.get("access_token", "") != "":
            self.token_info = AqaraTokenInfo(resp.json())
            resp.close
            return True

        resp.close
        return False
        
        # {'access_token': '6df0a7753ff1c4fb30b19607f28af7ff', 'refresh_token': '487934062f14cb16ba25353392d3bbf4', 'openId': '039837959257933685411465277441', 'state': 'aiot', 'token_type': 'bearer', 'expires_in': 604800}

    def is_connect(self) -> bool:
        """Is connect to aqara cloud."""
        return self.token_info is not None and len(self.token_info.access_token) > 0

    def query_all_page(self, body, callback):
        has_next = True
        # device_list : dict[str, AqaraDevice] = {}
        count: int = 0

        while has_next:
            resp = self.post(PATH_OPEN_API, body)
            if self.__get_code(resp) != 0:
                has_next = False
                return

            result = resp.get("result", {})
            data = result.get("data", {})

            count = count + len(data)
            total_count = result.get("totalCount", 0)
            if total_count <= 0 or count >= total_count:
                has_next = False

            body["data"]["pageNum"] = body["data"]["pageNum"] + 1
            callback(data)

    def __request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        if method == "POST" and path is PATH_OPEN_API and body is not None:
            self.__refresh_access_token_if_need(body["intent"])

        nonce = self.__nonce()
        t = self.__timestamp()
        sign = self.__calculate_sign(nonce, t)
        headers = {
            # "Accesstoken": self.token_info.access_token,
            "Appid": self.app_id,
            "Keyid": self.key_id,
            "Nonce": nonce,
            "Time": t,
            "Sign": sign,
        }
        if self.token_info is not None and self.token_info.access_token != "":
            headers["Accesstoken"] = self.token_info.access_token
        # logger.debug(f"sign:{sign}")

        # Accesstoken String	否	通过授权获取的访问Token
        # Appid	String	        是	第三方应用的Appid
        # Keyid	String	        是	appKey对应id
        # Nonce String	        是	随机字符串，每次请求都不同
        # Time	String	        是	请求时间戳，单位毫秒
        # Sign	String	        是	请求签名
        # Lang	Enum	        否	语言，默认英文，'zh', 'en'

        # logger.debug(
        #     f"Request: method = {method}, \
        #         url = {self.endpoint + path},\
        #         params = {params},\
        #         body = {filter_logger(body)},\
        #         t = {t}"
        # )

        response =  self.session.request(
            method, self.endpoint + path, params=params, json=body, headers=headers
        )

        if response.ok is False:
            if hasattr(response, "body"):
                logger.error(
                    f"Response error: code={response.status_code}, body={response.body}"
                )
            else:
                logger.error(
                    f"Response error: code={response.status_code}, request:{body}"
                )
            return None

        result = response.json()

        # logger.debug(
        #     f"Response: {json.dumps(filter_logger(result), ensure_ascii=False, indent=2)}"
        # )

        if result.get("code", -1) == AQARA_ERROR_CODE_ACCESSTOKEN_INCORRECT:
            self.token_info = None
            self.connect(
                self.__username, self.__password, self.__country_code, self.__schema
            )
        return result

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Http Get.

        Requests the server to return specified resources.

        Args:
            path (str): api path
            params (map): request parameter

        Returns:
            response: response body
        """
        return self.__request("GET", path, params, None)

    def post(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Http Post.

        Requests the server to update specified resources.

        Args:
            path (str): api path
            body (map): request body

        Returns:
            response: response body
        """
        try:
            return self.__request("POST", path, None, body)
        except:
            logger.error("post error")
            return {}

    def put(self, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        """Http Put.

        Requires the server to perform specified operations.

        Args:
            path (str): api path
            body (map): request body

        Returns:
            response: response body
        """
        return self.__request("PUT", path, None, body)

    def delete(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Http Delete.

        Requires the server to delete specified resources.

        Args:
            path (str): api path
            params (map): request param

        Returns:
            response: response body
        """
        return self.__request("DELETE", path, params, None)