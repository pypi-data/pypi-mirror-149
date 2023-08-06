from dataclasses import dataclass

from core.number.BigFloat import BigFloat


@dataclass
class Position:
    instrument: str
    quantity: BigFloat
    instant: int
    exchanged_from: str = None
