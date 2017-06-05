# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from bhojanusers.models import Customer, CustomerAddress, DeliveryExecutive
from bhojanmenu.models import Food

ORDERSTATUS = (
	('placed', 'placed'),
	('prepared', 'prepared'),
	('out_for_delivery', 'out_for_delivery'),
	('delivered', 'delivered'),
	('cancelled', 'cancelled')
	)


class Order(models.Model):
    customer = models.ForeignKey(Customer)
    amount = models.FloatField(default=0.0)
    order_time = models.DateTimeField()
    delivery_executive = models.ForeignKey(DeliveryExecutive, null=True, blank=True)
    delivery_address = models.ForeignKey(CustomerAddress)
    status = models.CharField(max_length=10, choices=ORDERSTATUS)


class OrderItems(models.Model):
    order = models.ForeignKey(Order)
    food = models.ForeignKey(Food)
    quantiy = models.IntegerField()
