import re
from django.core.exceptions import ValidationError


def validate_plate_alpha_end(plate_number):
    if not re.findall(r'[A-Z]', plate_number[-1]):
        raise ValidationError(
            'Plate must have an uppercase letter at the end.'
        )
    return plate_number


def validate_plate_number(plate_number):
    if not re.findall(r'^(?!0)(\d{4})', plate_number):
        raise ValidationError(
            'Plate starts with number from 1000 to 9999 before the letter.'
        )
    return plate_number
