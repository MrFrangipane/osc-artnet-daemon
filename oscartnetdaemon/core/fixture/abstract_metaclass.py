from abc import ABCMeta
from dataclasses import is_dataclass


class AbstractFixtureMetaclass(ABCMeta):
    def __new__(mcs, name, bases, attrs):
        new_cls = super().__new__(mcs, name, bases, attrs)

        for attr_name, attr_value in attrs.items():
            if attr_name == 'Mapping' and is_dataclass(attr_value):
                break
        else:
            raise NameError(f"Class '{name}' does not have a nested dataclass named 'Mapping'")

        return new_cls
