import os
import typing

from . import exceptions


def config_path_exists(
    *,
    config_path: typing.Optional[str] = None,
    config_path_env_var: typing.Optional[str] = None,
    default_config_path: typing.Optional[str] = None,
) -> bool:
    config_path = get_config_path(
        config_path=config_path,
        config_path_env_var=config_path_env_var,
        default_config_path=default_config_path,
        raise_if_dne=False,
    )
    return os.path.isfile(config_path)


def get_config_path(
    *,
    config_path: typing.Optional[str] = None,
    config_path_env_var: typing.Optional[str] = None,
    default_config_path: typing.Optional[str] = None,
    raise_if_dne: bool = True,
) -> str:

    # validate input combination
    if config_path is not None and config_path_env_var is not None:
        raise Exception('cannot specify config_path and config_path_env_var')

    # get config_path from environmental variable
    if config_path_env_var is not None:
        config_path = os.environ.get(config_path_env_var)
        if config_path == '':
            config_path = None

    # use default config path if not specified
    if config_path is None and default_config_path is not None:
        config_path = default_config_path

    # validate config_path
    if config_path is None:
        raise exceptions.ConfigPathUnset('config path is not set')
    else:
        if raise_if_dne and not os.path.isfile(config_path):
            raise exceptions.ConfigDoesNotExist(
                'config at path does not exist: ' + str(config_path)
            )

    return config_path

