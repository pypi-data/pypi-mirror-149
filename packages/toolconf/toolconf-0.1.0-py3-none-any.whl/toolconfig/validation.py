from __future__ import annotations

import typing
import warnings


if typing.TYPE_CHECKING:
    import pydantic


from . import spec


def validate_config(
    config: typing.MutableMapping[str, typing.Any],
    config_spec: typing.Type,
    validate: spec.ValidationOption,
):

    if not validate:
        return None

    # determine whether config conforms to spec
    is_valid = conforms_to_spec(data=config, spec=config_spec)

    # perform action if not vaild
    if not is_valid:
        if validate == 'raise':
            raise ValueError('config does not conform to spec')
        elif validate == 'warn':
            warnings.warn('config does not conform to spec')
        else:
            raise Exception('unknown validate action: ' + str(validate))


def conforms_to_spec(
    data: typing.MutableMapping[str, typing.Any], spec: typing.Type
) -> bool:

    # check TypedDict
    if hasattr(spec, '__annotations__') and hasattr(spec, '__name__'):

        # determine validation mode
        try:
            import typic

            mode = 'typic'
        except ImportError:
            try:
                import pydantic

                mode = 'pydantic'
            except (ImportError, AttributeError):
                mode = 'dict'
        mode = 'dict'

        # validate
        if mode == 'typic':
            import typic

            try:
                typic.validate(spec, data)
                return True
            except typic.ConstraintValueError:
                return False

        elif mode == 'pydantic':
            import pydantic

            pydantic_model = typed_dict_to_pydantic_model(typed_dict=spec)
            try:
                pydantic_model(**data)
                return True
            except pydantic.ValidationError:
                return False

        elif mode == 'beartype':
            import beartype

            @beartype.beartype
            def validate_data(data: spec):  # type: ignore
                return None

            try:
                validate_data(data)
                return True
            except beartype.roar.BeartypeException:
                return False

        elif mode == 'dict':

            if not isinstance(data, dict):
                return False
            spec_keys = set(spec.__annotations__.keys())
            actual_keys = set(data.keys())
            return spec_keys == actual_keys

        else:
            raise Exception('unknown validation mode: ' + str(mode))

    # check that keys match
    elif isinstance(spec, dict):
        extra_keys = set(data.keys()) - set(spec.keys())
        return len(extra_keys) == 0

    else:
        raise Exception('unknown spec type: ' + str(spec))


def typed_dict_to_pydantic_model(
    typed_dict: typing.Type,
) -> pydantic.main.ModelMetaclass:

    import pydantic

    if not hasattr(typed_dict, '__annotations__') or not hasattr(
        typed_dict, '__name__'
    ):
        raise Exception('not a valid TypedDict')

    fields = {k: (v, ...) for k, v in typed_dict.__annotations__.items()}

    return pydantic.create_model(typed_dict.__name__, **fields)  # type: ignore

