from dataclasses import dataclass, field
from enum import Enum

from core.number.BigFloat import BigFloat


class Status(Enum):
    NEW = 'new'
    CANCELLED = 'cancelled'
    EXECUTED = 'executed'
    ERROR = 'error'


class OrderType(Enum):
    LIMIT = 'limit'
    MARKET = 'market'


@dataclass
class Order:
    instrument_from: str
    instrument_to: str
    quantity: BigFloat
    order_id: str
    order_type: OrderType
    status: Status
    interval: int
