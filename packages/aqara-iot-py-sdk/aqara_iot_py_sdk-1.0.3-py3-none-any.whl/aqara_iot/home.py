"""Aqara home's api base on asset and device api."""
from __future__ import annotations
from types import SimpleNamespace
from typing import Any

from aqara_iot.aqara_enums import PATH_OPEN_API
from .device import AqaraDeviceManager
from .openapi import AqaraOpenAPI

# from .openmq import AqaraOpenMQ


class AqaraScene(SimpleNamespace):
    """Aqara Scene.
    Attributes:
    """

    def __init__(self, scene):
        # scene_map[item["sceneId"]] = item   # {"positionId":"","localizd": 0, "sceneId": "AL.832619739930738688",        "name": "123456",       "model": "app.scene.v1"   }
        self.scene_id = scene["sceneId"]
        self.position_id = scene["positionId"]
        self.name = scene["name"]
        self.enabled = True
        self.localizd = scene["localizd"]

    scene_id: str
    position_id: str
    name: str
    # actions: list
    enabled: bool  # 缺少是否enable
    localizd: int  # 0:云端 1:本地 3：云端化中 4：本地化中


class AqaraHomeManager:
    """Aqara Home Manager."""

    def __init__(
        # self, api: AqaraOpenAPI, mq: AqaraOpenMQ, device_manager: AqaraDeviceManager
        self,
        api: AqaraOpenAPI,
        device_manager: AqaraDeviceManager,
    ):
        """Init aqara home manager."""
        self.api = api
        # self.mq = mq
        self.device_manager = device_manager
        self.location_map = {}

        # #更新设备位置名称
        # for device in self.device_manager.device_map.values():
        #     device.position_name = self.location_map.get(device.position_id,"")

    def update_device_cache(self):
        """Update home's devices cache."""
        self.device_manager.device_map.clear()
        self.device_manager.generate_devices_and_update_value()

    def query_scenes(self) -> list:
        """Query scenes."""
        scenes: list[AqaraScene] = []

        scene_map = self._query_all_scene()
        for scene_id in scene_map.keys():
            scenes.append(AqaraScene(scene_map[scene_id]))
        return scenes

    def update_location_info(self) -> None:
        """Query location."""
        self.location_map = self._query_location_info("", True)
        for device in self.device_manager.device_map.values():
            device.position_name = self.location_map.get(device.position_id, "")

    # def get_location_name(self, position_id:str) -> str :
    #     if self.location_map.get(position_id) is None:
    #         sub_local_map = self._query_location_info(position_id, query_sub_location = False)
    #         self.location_map.update(sub_local_map)

    #     return self.location_map.get(position_id, "")

    def trigger_scene(self, position_id: str, scene_id: str) -> dict[str, Any]:
        """Trigger home scene"""
        body = {"intent": "config.scene.run", "data": {"sceneId": scene_id}}
        return self.api.post(PATH_OPEN_API, body)

    def _query_location_info(
        self, parent_position_id: str, query_sub_location: bool
    ) -> dict[str, str]:
        body = {
            "intent": "query.position.info",
            "data": {
                "parentPositionId": parent_position_id,  # 父位置ID，为空则查询用户/项目下所有顶级位置id
                "pageNum": 1,
                "pageSize": 50,
            },
        }

        def __result_handler(data):
            for item in data:
                position_id = item["positionId"]
                pisition_map[position_id] = item["positionName"]
                if query_sub_location:
                    sub_local_map = self._query_location_info(
                        position_id, query_sub_location
                    )
                    pisition_map.update(sub_local_map)

        pisition_map: dict[str, str] = {}
        self.api.query_all_page(body, __result_handler)
        return pisition_map

    def _query_all_scene(self) -> dict[str, Any]:
        location_map = self._query_location_info("", True)
        scene_map: dict[str, Any] = {}
        for position_id in location_map.keys():
            scenes = self._query_scene_by_location(position_id)
            scene_map.update(scenes)

        return scene_map

    def _query_scene_by_location(self, position_id: str) -> dict[str, Any]:
        body = {
            "intent": "query.scene.listByPositionId",
            "data": {"positionId": position_id, "pageNum": 1, "pageSize": 50},
        }

        def __result_handler(data):
            for item in data:
                item["positionId"] = position_id
                scene_map[
                    item["sceneId"]
                ] = item  # {"localizd": 0, "sceneId": "AL.832619739930738688",        "name": "123456",       "model": "app.scene.v1"   }

        scene_map: dict[str, Any] = {}
        self.api.query_all_page(body, __result_handler)
        return scene_map
