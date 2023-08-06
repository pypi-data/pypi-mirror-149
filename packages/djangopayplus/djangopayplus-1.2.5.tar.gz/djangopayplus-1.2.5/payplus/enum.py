from enum import IntEnum


class StatusTypes(IntEnum):
    ACTIVE = 1
    PENDING = 2
    DELETED = 3
    COMPLETED = 4
    FAILED = 5
    PROCESSING = 6
    DISAPPROVED = 7
    PAYMENTPENDING = 8
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class NetworkTypes(IntEnum):
    MTN = 0
    VODAFONE = 1
    AIRTELTIGO = 2
    GLO = 3
    EXPRESSO = 4
    UNKNOWN = 5

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def choicesAsDict(cls):
        return {key.value: key.name for key in cls}
    
    @classmethod
    def dichoices(cls):
        return {key.name:key.value for key in cls}