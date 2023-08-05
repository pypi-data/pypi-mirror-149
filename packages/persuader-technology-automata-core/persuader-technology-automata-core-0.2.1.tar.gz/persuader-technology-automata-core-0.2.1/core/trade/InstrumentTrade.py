from dataclasses import dataclass, field
from enum import Enum

from core.number.BigFloat import BigFloat


class Status(Enum):
    NEW = 'new'
    SUBMITTED = 'submitted'
    CANCELLED = 'cancelled'
    EXECUTED = 'executed'
    ERROR = 'error'


@dataclass
class InstrumentTrade:
    instrument_from: str
    instrument_to: str
    quantity: BigFloat
    status: Status = field(default=Status.NEW)
    description: str = field(default=None)
    order_id: str = field(default=None)
