import datetime
from typing import Dict, Union
from abc import ABC
import pprint


class RestObject(ABC):
    prop_types: "Dict[str, Union[type, str]]" = {}
    attribute_map: "Dict[str, Union[type, str]]" = {}

    def to_dict(self):
        result = {}

        for attr, attrKey in self.attribute_map.items():
            if hasattr(self, attr):
                value = getattr(self, attr)
                result[attrKey] = self.__serialize(value)
        if issubclass(type(self), dict):
            for key, value in self.items():
                result[key] = self.__serialize(value)

        return result

    def __serialize(self, obj):
        if isinstance(obj, list):
            return list(map(lambda x: self.__serialize(x), obj))

        if hasattr(obj, "to_dict"):
            return obj.to_dict()

        if isinstance(obj, dict):
            return dict(
                map(
                    lambda item: (item[0], self.__serialize(item[1])),
                    obj.items(),
                )
            )

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if issubclass(type(obj), dict):
            result = {}
            for key, value in obj.items():
                result[key] = value

            return result

        return obj

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, type(self)):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
