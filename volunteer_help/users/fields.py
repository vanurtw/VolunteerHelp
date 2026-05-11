from django.db import models
from .validators import validate_phone_number


class PhoneField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 16)
        kwargs.setdefault('validators', [validate_phone_number])
        super().__init__(*args, **kwargs)
