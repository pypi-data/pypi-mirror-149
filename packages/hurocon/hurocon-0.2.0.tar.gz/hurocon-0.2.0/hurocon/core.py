from pathlib import Path
from shutil import rmtree
from base64 import b64encode, b64decode

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from huawei_lte_api.enums.device import ControlModeEnum

from serialix import JSON_Format


LOCAL_CONFIG_PATH = Path.home() / Path('.config/hurocon/config.json')
LOCAL_CONFIG_DEFAULT = {
    "config_version": 2,
    "connection_address": "http://192.168.8.1/",
    "auth": {
        "username": "admin",
        "password": "YWRtaW4="
    }
}

_config_update_checked = False


class LocalConfig(JSON_Format):
    def __init__(self, **kwargs):
        super().__init__(
            LOCAL_CONFIG_PATH, LOCAL_CONFIG_DEFAULT,
            parser_write_kwargs={"indent": 4},
            **kwargs
        )

        if self.file_exists():
            self.__check_updates()

    def __check_updates(self):
        global _config_update_checked

        if not _config_update_checked:
            local_version = self['config_version']
            if local_version < LOCAL_CONFIG_DEFAULT['config_version']:
                if local_version < 2:
                    self['connection_address'] = 'http://{}/'.format(
                        self['connection_ip']
                    )

                    del(self['connection_ip'])

                    self['auth']['password'] = b64encode(
                        self['auth']['password'].encode()
                    ).decode()

                self['config_version'] = LOCAL_CONFIG_DEFAULT['config_version']
                self.commit()

            _config_update_checked = True

    @staticmethod
    def erase_config() -> bool:
        """
        Erase all local configuration files and dirs

        :return: Do the existing file was successfully removed
        :rtype: bool
        """
        result = False

        if LOCAL_CONFIG_PATH.parent.exists():
            rmtree(LOCAL_CONFIG_PATH.parent)
            result = True

        return result


class AuthConfig():
    username = ""
    connection_address = ""

    def __init__(self) -> None:
        self.__cfg = LocalConfig()
        self.username = self.__cfg['auth']['username']
        self.__password = self.__cfg['auth']['password']
        self.connection_address = self.__cfg['connection_address']

    def commit(self):
        self.__cfg['auth']['username'] = self.username
        self.__cfg['auth']['password'] = self.__password
        self.__cfg['connection_address'] = self.connection_address
        self.__cfg.commit()

    def reset(self):
        self.__cfg.reset_to_defaults()
        self.__cfg.commit()

    @property
    def password(self) -> str:
        return b64decode(self.__password).decode()

    @password.setter
    def password(self, passwd: str) -> None:
        self.__password = b64encode(passwd.encode()).decode()


class HLC_Connection(Connection):
    def __init__(self):
        auth_cfg = AuthConfig()
        super().__init__(
            url=auth_cfg.connection_address,
            username=auth_cfg.username,
            password=auth_cfg.password
        )


def test_connection() -> str:
    """
    Test connection to router with details from configuration file

    :return: "ok" if successfully connected or the reason of failure
    :rtype: str
    """
    result = 'ok'
    try:
        with HLC_Connection() as router_con:
            Client(router_con)
    except Exception as e:
        result = e

    return result


def reboot_router() -> None:
    with HLC_Connection() as router_con:
        client = Client(router_con)
        client.device.set_control(ControlModeEnum.REBOOT)


def sms_send(number, text: str) -> str:
    with HLC_Connection() as router_con:
        return Client(router_con).sms.send_sms(
            [number],
            text
        )
