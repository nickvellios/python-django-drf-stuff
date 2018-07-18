from .models import Employee, Payroll
from rest_framework import serializers

class PayrollSerializer(serializers.ModelSerializer):
	approved_by = serializers.ReadOnlyField(source='approved_by.email')

	class Meta:
		model = Payroll
		fields = ('week', 'pay_rate', 'amount', 'approved_by', 'employee')
		extra_kwargs = {'employee': {'required': False}}

class EmployeeSerializer(serializers.ModelSerializer):
	payrolls = PayrollSerializer(many=True, read_only=True)

	class Meta:
		model = Employee
		fields = ('id', 'name', 'date_of_hire', 'pay_rate', 'payrolls')
