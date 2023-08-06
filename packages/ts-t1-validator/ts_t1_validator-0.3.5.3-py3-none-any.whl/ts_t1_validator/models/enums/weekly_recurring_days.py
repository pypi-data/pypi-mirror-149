from enum import Enum, unique


@unique
class WeeklyRecurringDaysEnum(Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    UNDEFINED = None

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)

    # noinspection PyTypeChecker
    @staticmethod
    def asList():
        return list(WeeklyRecurringDaysEnum)
