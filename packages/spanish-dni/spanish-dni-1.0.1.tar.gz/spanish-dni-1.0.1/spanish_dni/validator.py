import re

from spanish_dni.constants import REGEXP, CONTROL_DIGIT, DNITypes, NIE_FIRST_DIGITS
from spanish_dni.dni import DNI
from spanish_dni.exceptions import NotValidDNIException


def _normalize_nie(dni: str) -> str:
    """
    :param dni: Validated DNI format
    :return: NIE normalized in NIF format
    """
    if DNI.get_dni_type(dni) == DNITypes.NIE:
        dni = NIE_FIRST_DIGITS[dni[0]] + dni[1:]
    return dni


def validate_dni(dni: str) -> DNI:
    """
    :param dni: raw string with DNI to validate
    :return: DNI object of validated data
    :raises: NotValidDNIException
    """
    dni: str = dni.upper()
    if not re.match(REGEXP, dni):
        raise NotValidDNIException
    dig_control: str = dni[8]
    dni_number: str = dni[:8]
    normalized_dni: str = _normalize_nie(dni_number)
    if not CONTROL_DIGIT[int(normalized_dni) % 23] == dig_control:
        raise NotValidDNIException
    return DNI(number=dni, control_digit=dig_control)
