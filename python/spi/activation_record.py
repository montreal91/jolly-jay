
from enum import Enum


class ArType(Enum):
    PROGRAM = "program"


class ActivationRecord:
    def __init__(self, name, ar_type, nesting_level):
        self._name = name
        self._type = ar_type
        self._nesting_level = nesting_level
        self._members = {}

    def __setitem__(self, key, value):
        self._members[key] = value

    def __getitem__(self, item):
        return self._members[item]

    def get(self, key):
        return self._members.get(key)

    def __str__(self):
        lines = [
            "{level}: {ar_type} {name}".format(
                level=self._nesting_level,
                ar_type=self._type,
                name=self._name
            )
        ]
        for name, val in self._members.items():
            lines.append(f"    {name:<20}: {val}")

        return "\n".join(lines)

    def __repr__(self):
        return self.__str__()
