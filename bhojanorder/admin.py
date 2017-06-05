# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Order, OrderItems

admin.site.register(Order)
admin.site.register(OrderItems)