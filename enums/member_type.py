from enum import Enum, auto


class MemberType(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    vendor = auto()
    consumer = auto()
