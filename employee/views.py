from rest_framework import generics
from .models import Employee, Payroll
from .serializers import EmployeeSerializer, PayrollSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import IsAdminOrOwner

class EmployeeList(generics.ListCreateAPIView):
	queryset = Employee.objects.all()
	serializer_class = EmployeeSerializer
	permission_classes = (IsAdminUser,)
	lookup_url_kwarg = 'employee_id'

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Employee.objects.all()
	serializer_class = EmployeeSerializer
	permission_classes = (IsAdminUser,)
	lookup_url_kwarg = 'employee_id'

class PayrollList(generics.ListCreateAPIView):
	serializer_class = PayrollSerializer
	permission_classes = (IsAdminUser,)
	lookup_url_kwarg = 'employee_id'

	def perform_create(self, serializer):
		serializer.save(
			approved_by=self.request.user,
			employee_id=self.kwargs['employee_id'])

	def get_queryset(self):
		employee = self.kwargs['employee_id']
		return Payroll.objects.filter(employee__id=employee)

class PayrollListAll(generics.ListCreateAPIView):
	queryset = Payroll.objects.all()
	serializer_class = PayrollSerializer
	permission_classes = (IsAdminUser,)
	lookup_url_kwarg = 'payroll_id'

class PayrollDetail(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = PayrollSerializer
	permission_classes = (IsAdminOrOwner,)
	lookup_url_kwarg = 'payroll_id'

	def get_queryset(self):
		payroll = self.kwargs['payroll_id']
		employee = self.kwargs['employee_id']
		return Payroll.objects.filter(id=payroll, employee__id=employee)