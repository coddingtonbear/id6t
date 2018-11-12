import json

import redis

from django.conf import settings
from django.db import models


class DataType(models.Model):
    MEASUREMENT_TYPES = [
        (
            'string',
            'String',
            lambda x: x
        ),
        (
            'float',
            'Float',
            lambda x: float(x)
        ),
        (
            'int',
            'Integer',
            lambda x: int(x)
        ),
        (
            'bool',
            'Boolean',
            lambda x: bool(x)
        ),
        (
            'pipe_delimited_float',
            'Pipe-delimited Float',
            lambda x: [float(v) for v in x.split('|')]
        ),
    ]

    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    type = models.CharField(
        max_length=255,
        choices=[
            (choice[0], choice[1]) for choice in MEASUREMENT_TYPES
        ]
    )

    @property
    def transformation(self):
        return list(filter(
            lambda x: x[0] == self.type,
            self.MEASUREMENT_TYPES
        ))[0][2]

    def __str__(self):
        return self.name


class DataSet(models.Model):
    id = models.UUIDField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        data = {
            'id': str(self.pk),
            'created': self.created.isoformat(),
        }
        for metric in self.metrics.all():
            data[metric.type.slug] = metric.value

        return data

    def __str__(self):
        return u'%s' % self.created


class Data(models.Model):
    type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    dataset = models.ForeignKey(
        DataSet,
        on_delete=models.CASCADE,
        related_name='metrics'
    )
    raw_value = models.CharField(max_length=255)

    @classmethod
    def create(cls, dataset_id, type_name, raw_value):
        dataset, _ = DataSet.objects.get_or_create(
            pk=dataset_id,
        )
        type, _ = DataType.objects.get_or_create(
            slug=type_name,
            defaults={
                'name': type_name,
                'type': 'string',
            }
        )
        # Make sure the value _can_ be transformed
        type.transformation(raw_value)

        return Data.objects.create(
            type=type,
            raw_value=raw_value,
            dataset=dataset
        )

    @property
    def value(self):
        return self.type.transformation(self.raw_value)

    def __str__(self):
        return u'%s: %s' % (
            self.type,
            self.value,
        )
