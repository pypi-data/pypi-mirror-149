"""Aqara iot enums."""

from dataclasses import dataclass
from enum import IntEnum

class AuthType(IntEnum):
    """Aqara Cloud Auth Type."""

    # Aqara账号授权:0、项目授权:1、虚拟账号授权:2
    AQARA_SMART_HOME = 0
    PROJECT = 1
    VIRTUAL = 2


AQARA_OAUTH2_AUTHORIZE = "/v3.0/open/authorize"

# 获取访问令牌
AQARA_OAUTH2_ACCESS_TOKEN = "/v3.0/open/access_token"


class AqaraCloudOpenAPIEndpoint:
    """Aqara Cloud Open API Endpoint."""

    # "/v3.0/open/api"

    # 中国大陆
    CHINA = "https://open-cn.aqara.com"
    #CHINA = "https://developer-test.aqara.com"

    # 美国
    AMERICA = "https://open-usa.aqara.com"

    # 韩国
    COREA = "https://open-kr.aqara.com"

    # 俄罗斯
    RUSSIA = "https://open-ru.aqara.com"

    # 欧洲
    EUROPE = "https://open-ger.aqara.com"


PATH_OPEN_API = "/v3.0/open/api"
PATH_AUTH = "/v3.0/open/authorize"
PATH_ACCESS_TOKEN = "/v3.0/open/access_token"


@dataclass
class AppInfo:
    """Describe App Info"""

    APP_ID: str
    APP_KEY: str
    KEY_ID: str


DEV = AppInfo(
    "948907588893974528e53aac",
    "gchwjfo48nd0da9d3nlne8iblxorbyzl",
    "K.948907589003026432",
)

#正式环境
CN = AppInfo(
    "941380790062239744112522",
    "tqvq2ol7va9v8u2w518qxedqxvx0e46i",
    "K.941380790108377088",
)
#测试环境
#CN =  AppInfo('948907588893974528e53aac','gchwjfo48nd0da9d3nlne8iblxorbyzl','K.948907589003026432')
RU = AppInfo(
    "948907588893974528e53aac",
    "gchwjfo48nd0da9d3nlne8iblxorbyzl",
    "K.948907589003026432",
)
EU = AppInfo(
    "948907588893974528e53aac",
    "gchwjfo48nd0da9d3nlne8iblxorbyzl",
    "K.948907589003026432",
)
US = AppInfo(
    "948907588893974528e53aac",
    "gchwjfo48nd0da9d3nlne8iblxorbyzl",
    "K.948907589003026432",
)
KR = AppInfo(
    "948907588893974528e53aac",
    "gchwjfo48nd0da9d3nlne8iblxorbyzl",
    "K.948907589003026432",
)
APPS: dict[str, AppInfo] = {
    "China": CN,
    "dev": DEV,
    "Europe": EU,
    "Russia": RU,
    "United States": US,
    "South Korea": KR,
}


EMPTY_PATH = ""


@dataclass
class Country:
    """Describe a supported country."""

    name: str
    country_code: str
    endpoint: str = AqaraCloudOpenAPIEndpoint.EUROPE


AQARA_COUNTRIES = [
    Country("China", "86", AqaraCloudOpenAPIEndpoint.CHINA),
    Country("Europe", "251", AqaraCloudOpenAPIEndpoint.EUROPE),
    Country("South Korea", "850", AqaraCloudOpenAPIEndpoint.COREA),
    Country("Russia", "7", AqaraCloudOpenAPIEndpoint.RUSSIA),
    Country("United States", "1", AqaraCloudOpenAPIEndpoint.AMERICA),
]
