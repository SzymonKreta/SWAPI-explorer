from django.db import models
from django.core.exceptions import ValidationError


def csv_hash_validator(name):
    if not name.endswith('.csv'):
        raise ValidationError


# Create your models here.
class DataSet(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    filename = models.CharField(max_length=36, validators=[csv_hash_validator])