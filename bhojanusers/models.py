# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User 


class Customer(models.Model):
	user = models.ForeignKey(User)
	full_name = models.CharField(max_length=50)
	phone_extension = models.CharField(max_length=10)
	phoneno = models.CharField(max_length=20)

	def __str__(self):
		return self.full_name

class CustomerAddress(models.Model):
	customer = models.ForeignKey(Customer)
	header = models.CharField(default="Home", max_length=25)
	address = models.TextField()
	lat_long = models.CharField(max_length=1024)

class DeliveryExecutive(models.Model):
	employee_id = models.CharField(max_length=6)
	user = models.ForeignKey(User)
	full_name = models.CharField(max_length=50)

	def __str__(self):
		return self.employee_id
