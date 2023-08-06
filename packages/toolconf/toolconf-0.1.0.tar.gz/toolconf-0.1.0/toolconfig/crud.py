from __future__ import annotations

import copy
import os
import typing

import toolcache

from . import filesystem
from . import spec
from . import validation


@toolcache.cache(cachetype='memory')
def get_config(
    config_path_env_var: typing.Optional[str] = None,
    config_path: typing.Optional[str] = None,
    default_config_path: typing.Optional[str] = None,
    config_spec: typing.Optional[typing.Type] = None,
    default_config_values: typing.Optional[dict] = None,
    config_required: bool = False,
    config_variables: typing.Optional[dict[str, typing.Mapping]] = None,
    validate: typing.Literal['raise', 'warn', False] = 'raise',
) -> spec.ConfigData:

    # get config path
    config_path = filesystem.get_config_path(
        config_path=config_path,
        config_path_env_var=config_path_env_var,
        default_config_path=default_config_path,
    )

    # load config
    config = None
    if config_path is not None:
        if not os.path.isfile(config_path):
            raise Exception('config file does not exist: ' + str(config_path))
        config = load_config_file(config_path)

    # check if config required
    if config_required and config is None:
        raise Exception(
            'must specify config, might need to set environment variable '
            + str(config_path_env_var)
        )

    # set defaults
    if default_config_values is None:
        default_config_values = {}
    if config is None:
        config = copy.deepcopy(default_config_values)
    for key, value in default_config_values.items():
        config.setdefault(key, value)

    # populate variables
    if config_variables is not None:
        for key, variables in config_variables.items():
            config[key] = config[key].format(**variables)

    # validate spec
    if validate:
        if config_spec is None:
            raise Exception('cannot validate unless config_spec is given')
        else:
            validation.validate_config(
                config=config,
                config_spec=config_spec,
                validate=validate,
            )

    return config


# for typing see https://github.com/python/mypy/issues/4441
def config_is_valid(**kwargs) -> bool:
    try:
        get_config(validate='raise', **kwargs)
        return True
    except ValueError:
        return False


def write_config_file(
    config_data: spec.ConfigData,
    path: str,
    overwrite: spec.OverwriteOption = False,
    style: typing.Optional[str] = None,
) -> None:

    if os.path.isfile(path):
        if overwrite is True:
            pass
        elif overwrite is False:
            raise Exception('use overwrite=True to overwrite an existing file')
        elif overwrite == 'prompt':
            import toolcli

            if not toolcli.input_yes_or_no(
                prompt='File already exists: '
                + str(path)
                + '\n\nOverwrite file?\n',
                style=style,
            ):
                raise Exception('must overwrite file to proceed')
        else:
            raise Exception('unknown value for overwrite: ' + str(overwrite))

    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)

    if path.endswith('.json'):
        import json

        with open(path, 'w') as f:
            json.dump(config_data, f)
    elif path.endswith('.toml'):
        import toml

        with open(path, 'w') as f:
            toml.dump(config_data, f)
    else:
        raise Exception('unknown file type: ' + str(path))


def load_config_file(config_path: str) -> spec.ConfigData:
    with open(config_path, 'r') as f:
        if config_path.endswith('.json'):
            import json

            return json.load(f)
        elif config_path.endswith('.toml'):
            import toml

            return toml.load(f)
        elif config_path.endswith('.yaml'):
            try:
                import yaml
            except ImportError:
                raise Exception(
                    'pyyaml required for yaml files, install using `pip install pyyaml`'
                )

            return yaml.load(f, Loader=yaml.CLoader)
        else:
            raise Exception('unknown config format')
