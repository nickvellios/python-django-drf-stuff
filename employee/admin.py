from django.contrib import admin
from .models import Employee, Payroll

class PayrollAdmin(admin.ModelAdmin):
	list_display = ('employee_name', 'week')


admin.site.register(Payroll, PayrollAdmin)
admin.site.register(Employee)
