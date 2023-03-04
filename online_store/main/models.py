from django.db import models

from django.db import models


class Citizen(models.Model):
    import_id = models.IntegerField()
    citizen_id = models.IntegerField()
    town = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    building = models.CharField(max_length=256)
    apartment = models.IntegerField()
    name = models.CharField(max_length=256)
    birth_date = models.DateField()
    gender = models.CharField(max_length=6)
    relatives = models.JSONField()


class Import(models.Model):
    created_date = models.DateField(auto_now_add=True)
    citizens = models.ManyToManyField(Citizen)
