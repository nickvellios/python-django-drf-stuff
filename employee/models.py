from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
	name = models.CharField(max_length=255)
	date_of_hire = models.DateTimeField('date of hire')
	pay_rate = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return self.name

class Payroll(models.Model):
	week = models.DateTimeField('date of paycheck')
	pay_rate = models.DecimalField(max_digits=6, decimal_places=2)
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	approved_by = models.ForeignKey(User)
	employee = models.ForeignKey(Employee, related_name='payrolls')

	def employee_name(self):
		return self.employee.name

	def __str__(self):
		return self.employee.name