from spanish_dni.constants import DNITypes, NIE_FIRST_DIGITS


class DNI:
    _number: str
    _control_digit: str
    dni_type: DNITypes

    def __init__(self, number: str, control_digit: str) -> None:
        self._number = number
        self._control_digit = control_digit
        self.dni_type = self.get_dni_type(self._number)

    @classmethod
    def get_dni_type(cls, dni: str) -> DNITypes:
        return DNITypes.NIE if dni[0] in NIE_FIRST_DIGITS.keys() else DNITypes.NIF
