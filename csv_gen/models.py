from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField

class Schema(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, related_name='schemas', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    modified_date = models.DateTimeField(auto_now_add=True, blank=True)

    class Delimeter(models.TextChoices):
        COMMA = ",", _('Comma (,)')
        TAB = "\t", _('Tab (   )')
        SEMICOLON = ";", _('Semicolon (;)')
        PIPE = "|", _('Pipe (|)')
    delimeter = models.CharField(
        max_length=20,
        choices=Delimeter.choices,
        default=Delimeter.COMMA,
    )

    class Quote(models.TextChoices):
        SINGLE = "'", _("Single-quote (')")
        DOUBLE = '"', _('Double-quote (")')
    quote = models.CharField(
        max_length=20,
        choices=Quote.choices,
        default=Quote.DOUBLE,
    )


class Dataset(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    schema = models.ForeignKey(
        Schema, on_delete=models.CASCADE, related_name='datasets')

    class Status(models.TextChoices):
        PROCCESSING = "Proccessing"
        READY = "Ready"

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PROCCESSING,
    )
    rows = models.IntegerField()


class Column(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    schema = models.ForeignKey(
        Schema, on_delete=models.CASCADE, related_name='columns')

    class Type(models.TextChoices):
        FULLNAME = 'Full name'
        JOB = 'Job'
        EMAIL = 'Email'
        DOMAINNAME = 'Domain name'
        PHONENUMBER = 'Phone number'
        COMPANYNAME = 'Company name'
        TEXT = 'Text'
        INTEGER = 'Integer'
        ADDRESS = 'Address'
        DATE = 'Date'

    col_type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.TEXT,
    )
    col_filter = JSONField()
    order = models.IntegerField(blank=True)

    class Meta:
        ordering = ['order']
