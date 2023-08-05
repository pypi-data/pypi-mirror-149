# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

from typing import Any

from pydantic import errors
from pydantic.fields import ModelField

from hagworm.extend import validator
from hagworm.extend.base import Utils


class _EnumKeyTypeBase(str):

    __subclasses__ = {}

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> int:

        if field.required is False and val == field.default:
            return val

        if not cls.Enum.has_key(val):
            raise errors.EnumMemberError(enum_values=cls.Enum)

        return getattr(cls.Enum, val).value


def EnumKeyType(enum):

    if enum not in _EnumKeyTypeBase.__subclasses__:

        _EnumKeyTypeBase.__subclasses__[enum] = type(
            r'EnumKeyType_{0}'.format(enum.__name__),
            (_EnumKeyTypeBase,),
            {r'Enum': enum}
        )

    return _EnumKeyTypeBase.__subclasses__.get(enum)


class _EnumValueTypeBase(int):

    __subclasses__ = {}

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> int:

        if field.required is False and val == field.default:
            return val

        if isinstance(val, int):
            pass
        elif val.isdigit():
            val = int(val)
        else:
            raise errors.EnumMemberError(enum_values=cls.Enum)

        if not cls.Enum.has_value(val):
            raise errors.EnumMemberError(enum_values=cls.Enum)

        return val


def EnumValueType(enum):

    if enum not in _EnumValueTypeBase.__subclasses__:

        _EnumValueTypeBase.__subclasses__[enum] = type(
            r'EnumValueType_{0}'.format(enum.__name__),
            (_EnumValueTypeBase,),
            {r'Enum': enum}
        )

    return _EnumValueTypeBase.__subclasses__.get(enum)


class IDCardType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not Utils.identity_card(val):
            raise ValueError(r'value is not a valid identity card')

        return val


class BankCardType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not Utils.luhn_valid(val):
            raise ValueError(r'value is not a valid bank card')

        return val


class UUIDType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not validator.uuid(val):
            raise errors.UUIDError()

        return val


class DateType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> Any:

        if field.required is False and val == field.default:
            return val

        try:
            val = Utils.date_parse(val)
        except Exception:
            raise errors.DateError()

        return val


class JsonType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> Any:

        if field.required is False and val == field.default:
            return val

        try:
            val = Utils.json_decode(val)
        except Exception:
            raise errors.JsonError()

        return val


class IntListType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> Any:

        if field.required is False and val == field.default:
            return val

        try:
            val = Utils.split_int(val)
        except Exception:
            raise errors.ListError()

        return val


class FloatListType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> Any:

        if field.required is False and val == field.default:
            return val

        try:
            val = Utils.split_float(val)
        except Exception:
            raise errors.ListError()

        return val


class ASCVisibleType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not validator.asc_visible(val):
            raise errors.StrRegexError(validator.REGEX_ASC_VISIBLE.pattern)

        return val


class EmailType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not validator.email(val):
            raise errors.EmailError()

        return val


class DomainType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not validator.domain(val):
            raise errors.UrlHostError()

        return val


class URLType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not validator.url(val):
            raise errors.UrlSchemeError()

        return val


class MacAddrType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not validator.mac_addr(val):
            raise ValueError(r'value is not a valid mac address')

        return val


class IPvAnyType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not validator.ipv4(val) or not validator.ipv6(val):
            raise errors.IPvAnyAddressError()

        return val


class IPv4Type(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not validator.ipv4(val):
            raise errors.IPv4AddressError()

        return val


class IPv4CidrType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not validator.ipv4_cidr(val):
            raise errors.IPv4AddressError()

        return val


class IPv6Type(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not validator.ipv6(val):
            raise errors.IPv6AddressError()

        return val


class IPv6CidrType(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, val: Any, field: ModelField) -> str:

        if field.required is False and val == field.default:
            return val

        if not validator.ipv6_cidr(val):
            raise errors.IPv6AddressError()

        return val
