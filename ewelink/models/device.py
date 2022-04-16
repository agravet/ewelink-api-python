from typing import Any, Iterable
from datetime import datetime
from dataclasses import dataclass

from .asset import Asset
from .enumerations import PowerState, DeviceType
from ..http import HttpClient

@dataclass
class Brand:
    name: str | None
    logo: Asset

@dataclass
class Network:
    ssid: str | None
    sta_mac: str | None

@dataclass
class Pulse:
    state: PowerState
    width: int

class Device:
    online_time: datetime | None
    offline_time: datetime | None

    def __init__(self, data: dict[str, str | int | Any], http: HttpClient | None = None) -> None:
        self.apikey: str | None = data.get('apikey', None)
        self.id: str = data.get('deviceid', '0')
        self.brand: Brand = Brand(
            name = data.get('brandName', None), 
            logo = Asset(data.get('brandLogoUrl', None), session=http.session if http else None)
        )
        self.url: str | None = data.get('deviceUrl', None)
        self.hash_id: str = data.get('_id', '0')
        self.created_at: datetime = datetime.strptime(data['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.key: str = data.get('devicekey', '0')
        self.name: str | None = data.get('name', None)
        self.online_time = None
        self.offline_time = None
        if online_time := data.get('onlineTime', None):
            self.online_time = datetime.strptime(online_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        if offline_time := data.get('offlineTime', None):
            self.offline_time = datetime.strptime(offline_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.state: PowerState = PowerState[data['params']['switch']]
        self.on_startup: PowerState = PowerState[data['params']['startup']] if data['params'].get('startup', None) else PowerState.off
        self.pulse: Pulse = Pulse(
            state=PowerState[data['params']['pulse']] if data['params'].get('pulse', None) else PowerState.off,
            width=data['params'].get('pulseWidth', 0)
        )
        self.network: Network = Network(
            ssid = data['params'].get('ssid', None),
            sta_mac = data['params'].get('staMac', None)
        )
        self.version: int = data['params'].get('version', 0)
        self.is_online: bool = data.get('online', False)
        self.location: str | None = data.get('location') if data.get('location', None) else None
        self.type: DeviceType = DeviceType.__dict__['_value2member_map_'].get(int(data.get('type', 0)), 0)

class Devices(list[Device]):
    def __init__(self, devices: Iterable[Device]):
        super().__init__(devices)

    def get(self, id: str) -> Device | None:
        for device in self:
            if device.id == id: return device