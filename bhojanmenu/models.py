# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

FOODCATEGORY = (
	('veg', 'veg'),
	('non-veg', 'non-veg'))

class Food(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    ingrediants = models.TextField()
    cuisine = models.CharField(max_length=50)
    category = models.CharField(max_length=10, choices=FOODCATEGORY)

    def __str__(self):
        return str(self.name)

class Menu(models.Model):
    food = models.ForeignKey(Food, related_name='menu')
    availability_start_time = models.DateTimeField()
    availability_end_time = models.DateTimeField()
    quantity = models.IntegerField()
    price = models.FloatField(default=0.0)
