# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone

def create_initial_employees(apps, schema_editor):
    Employee = apps.get_model('employee', 'Employee')

    Employee(name='Nick Vellios', pay_rate='16.50', date_of_hire=timezone.now()).save()
    Employee(name='Aurora Vellios', pay_rate='12.50', date_of_hire=timezone.now()).save()
    Employee(name='Jordan Vellios', pay_rate='14.50', date_of_hire=timezone.now()).save()

class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_payroll'),
    ]

    operations = [
        migrations.RunPython(create_initial_employees)
    ]
