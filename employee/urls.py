from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	# /employees/
	url(r'^employees/$', views.EmployeeList.as_view(), name="employee-list"),

	# /employees/<employee_id>/
	url(
		r'^employees/(?P<employee_id>[0-9]+)/$',
		views.EmployeeDetail.as_view(),
		name='employee-detail'
	),
	# /employees/<employee_id>/payroll/
	url(
		r'^employees/(?P<employee_id>[0-9]+)/payroll/$',
		views.PayrollList.as_view(),
		name='payroll-list'
	),

	# /payroll/
	url(r'^payroll/$', views.PayrollListAll.as_view()),

	# /employees/<employee_id>/payroll/<payroll_id>/
	url(
		r'^employees/(?P<employee_id>[0-9]+)/payroll/(?P<payroll_id>[0-9]+)/$',
		views.PayrollDetail.as_view(),
		name='payroll-detail'
	),
]

urlpatterns = format_suffix_patterns(urlpatterns)

