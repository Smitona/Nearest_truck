import re
from django.core.exceptions import ValidationError


class PlateAlphaEnd(object):
    def validate(self, plate_number,):
        if not re.findall(r'[A-Z]', plate_number[-1]):
            raise ValidationError(
                'Plate must have an uppercase letter at the end.'
            )

    def get_help_text(self):
        return 'Plate number must have an uppercase letter at the end.'


class PlateNumber(object):
    def validate(self, plate_number,):
        if not re.findall(r'^(?!0)(\d{4})', plate_number):
            raise ValidationError(
                'Plate starts with number from 1000 to 9999 before the letter.'
            )

    def get_help_text(self):
        return 'Plate starts with number from 1000 to 9999 before the letter.'
