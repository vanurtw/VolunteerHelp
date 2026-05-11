import re
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not re.match(r'\+7\d{10}$', value):
        raise ValidationError("Номер должен быть в формате +7XXXXXXXXXX")
