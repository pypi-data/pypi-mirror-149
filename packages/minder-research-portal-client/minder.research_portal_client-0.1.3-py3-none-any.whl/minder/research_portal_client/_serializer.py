import datetime
import json
import re
from typing import Type, TypeVar, Union, final
import minder.research_portal_client.models as models
from minder.research_portal_client._utils import RestObject


_T = TypeVar("_T")


@final
class Serializer(object):
    PRIMITIVE_TYPES = (float, bool, bytes, str, int)
    NATIVE_TYPES_MAPPING = {
        "int": int,
        "long": int,
        "float": float,
        "str": str,
        "bool": bool,
        "date": datetime.date,
        "datetime": datetime.datetime,
        "object": object,
    }

    def serialize(self, obj: RestObject, *, indent: int = None) -> str:
        return json.dumps(obj.to_dict(), indent=indent)

    def deserialize(self, data, response_type: Union[Type[_T], str]) -> _T:
        return self.__deserialize(data, response_type)

    def __deserialize(self, data, klass: "Union[Type, str]"):
        if data is None:
            return None

        if isinstance(klass, str):
            if klass.startswith("list["):
                match = re.match(r"list\[(.*)\]", klass)
                sub_kls = match.group(1) if match is not None else list
                return [self.__deserialize(sub_data, sub_kls) for sub_data in data]

            if klass.startswith("dict("):
                match = re.match(r"dict\(([^,]*), (.*)\)", klass)
                sub_kls = match.group(2) if match is not None else dict
                return {k: self.__deserialize(v, sub_kls) for k, v in data.items()}

            if klass in self.NATIVE_TYPES_MAPPING:
                klass = self.NATIVE_TYPES_MAPPING[klass]
            else:
                klass = getattr(models, klass)

        if klass in self.PRIMITIVE_TYPES:
            return self.__deserialize_primitive(data, klass)

        if klass == object:
            return data

        if klass == datetime.date:
            return self.__deserialize_date(data)

        if klass == datetime.datetime:
            return self.__deserialize_datetime(data)

        return self.__deserialize_model(data, klass)

    def __deserialize_primitive(self, data, klass):
        try:
            return klass(data)
        except UnicodeEncodeError:
            return str(data)
        except TypeError:
            return data

    def __deserialize_date(self, string):
        try:
            from dateutil.parser import parse

            return parse(string).date()
        except ImportError:
            return string
        except ValueError:
            raise ValueError("Failed to parse `{0}` as date object".format(string))

    def __deserialize_datetime(self, string):
        try:
            from dateutil.parser import parse

            return parse(string)
        except ImportError:
            return string
        except ValueError:
            raise ValueError("Failed to parse `{0}` as datetime object".format(string))

    def __hasattr(self, object, name):
        return name in object.__dict__ or name in object.__class__.__dict__

    def __deserialize_model(self, data, klass):
        if not klass.prop_types and not self.__hasattr(klass, "get_real_child_model"):
            return data

        kwargs = {}
        if klass.prop_types is not None:
            for attr, attr_type in klass.prop_types.items():
                if data is not None and klass.attribute_map[attr] in data and isinstance(data, (list, dict)):
                    value = data[klass.attribute_map[attr]]
                    kwargs[attr] = self.__deserialize(value, attr_type)

        instance = klass(**kwargs)

        if isinstance(instance, dict) and klass.prop_types is not None and isinstance(data, dict):
            for key, value in data.items():
                if key not in klass.prop_types:
                    instance[key] = value
        if self.__hasattr(instance, "get_real_child_model"):
            klass_name = instance.get_real_child_model(data)
            if klass_name:
                instance = self.__deserialize(data, klass_name)
        return instance
