from enum import Enum
from typing import Set, Dict

REGEXP: str = r"[0-9XYZ]{8}[TRWAGMYFPDXBNJZSQVHLCKE]"
CONTROL_DIGIT: str = "TRWAGMYFPDXBNJZSQVHLCKE"
NOT_ACCEPTED: Set[str] = {"00000000T", "00000001R", "99999999R"}
NIE_FIRST_DIGITS: Dict[str, str] = {"X": "0", "Y": "1", "Z": "2"}


class DNITypes(Enum):
    NIF = "NIF"
    NIE = "NIE"
