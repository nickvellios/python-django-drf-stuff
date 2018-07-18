# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('date_of_hire', models.DateTimeField(verbose_name=b'date of hire')),
                ('pay_rate', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week', models.DateTimeField(verbose_name=b'date of paycheck')),
                ('pay_rate', models.DecimalField(max_digits=6, decimal_places=2)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('approved_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(to='employee.Employee')),
            ],
        ),
    ]
