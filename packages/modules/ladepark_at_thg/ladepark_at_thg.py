#!/usr/bin/env python3
import logging

from modules.ladepark_at_thg.config import LadeparkAtThgConfiguration
from modules.common.abstract_device import DeviceDescriptor
from typing import TypeVar, Generic, Callable
from modules.common import req

log = logging.getLogger(__name__)

T_LADEPARK_AT_THG_CONFIG = TypeVar("T_LADEPARK_AT_THG_CONFIG")


class ConfigurableLadeparkAtThg(Generic[T_LADEPARK_AT_THG_CONFIG]):
    def __init__(self,
                 config: T_LADEPARK_AT_THG_CONFIG,
                 component_updater: Callable[[str, bytes], None]) -> None:
        self.__component_updater = component_updater
        self.config = config

    def update(self, mac_address: str, backup_filename: str, backup_file: bytes):
        self.__component_updater(mac_address, backup_filename, backup_file)


def upload_data(config: LadeparkAtThgConfiguration, mac_address: str, backup_filename: str, backup_file: bytes) -> None:
    req.get_http_session().put(
        f'{config.server_url}?macaddress={mac_address}&filename={backup_filename}',
        headers={'X-Requested-With': 'XMLHttpRequest', "X-API-Key": config.api_key},
        data=backup_file,
    )


def create_ladepark_at_thg(config: LadeparkAtThgConfiguration):
    def updater(mac_address: str, backup_filename: str, backup_file: bytes):
        upload_data(config, mac_address, backup_filename, backup_file)
    return ConfigurableLadeparkAtThg(config=config, component_updater=updater)


device_descriptor = DeviceDescriptor(configuration_factory=LadeparkAtThgConfiguration)
