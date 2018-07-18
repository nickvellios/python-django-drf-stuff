import pytest
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from employee.models import Employee, Payroll
from django.utils import timezone


UserModel = get_user_model()

class APIAdminAPITestCase(APITestCase):
	@pytest.mark.django_db
	def setUp(self):
		self.user = UserModel.objects.create_superuser(
			username='test', email='test@...', password='top_secret')
		token = Token.objects.create(user=self.user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class APIUserAPITestCase(APITestCase):
	@pytest.mark.django_db
	def setUp(self):
		self.user = UserModel.objects.create_user(
			username='test', email='test@...', password='top_secret')
		token = Token.objects.create(user=self.user)
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

		# Create a payroll entry for an employee
		url = reverse('payroll-list', kwargs={'employee_id': 1})
		data = {
			"week": timezone.now(),
			"pay_rate": 17.25,
			"amount": 890
		}
		self.client.post(url, data, format='json')

class TestEmployeeListAnonymous(APITestCase):
	@pytest.mark.django_db
	def test_can_get_employee_list(self):
		url = reverse('employee-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(len(response.data), 1)


class TestEmployeeListAdmin(APIAdminAPITestCase):
	@pytest.mark.django_db
	def test_admin_can_post_new_employee(self):
		url = reverse('employee-list')

		data = {
			"name": "Frank Smith",
			"date_of_hire": timezone.now(),
			"pay_rate": "8.50"
		}

		response = self.client.post(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Employee.objects.count(), 4)

	@pytest.mark.django_db
	def test_anonymous_cannot_post_new_employee(self):
		url = reverse('employee-list')

		data = {
			"name": "Frank Smith",
			"date_of_hire": timezone.now(),
			"pay_rate": "8.50"
		}

		self.client.logout()
		response = self.client.post(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(Employee.objects.count(), 3)

class TestEmployeeDetailAnonymous(APITestCase):
	@pytest.mark.django_db
	def test_can_get_employee_detail(self):
		url = reverse('employee-detail', kwargs={'employee_id': 1})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestEmployeeDetailAdmin(APIAdminAPITestCase):
	@pytest.mark.django_db
	def test_admin_can_delete_an_employee(self):
		url = reverse('employee-detail', kwargs={'employee_id': 1})

		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Employee.objects.count(), 2)

	@pytest.mark.django_db
	def test_anonymous_cannot_delete_an_employee(self):
		url = reverse('employee-detail', kwargs={'employee_id': 1})

		# Logout so the user is anonymous
		self.client.logout()

		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(Employee.objects.count(), 3)

	@pytest.mark.django_db
	def test_admin_can_update_an_employee(self):
		url = reverse('employee-detail', kwargs={'employee_id': 1})

		data = {
			"name": "Frank R Smith",
			"date_of_hire": timezone.now(),
			"pay_rate": "8.60"
		}

		response = self.client.put(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Employee.objects.count(), 3)
		self.assertEqual(response.data['pay_rate'], '8.60')
		self.assertEqual(response.data['name'], 'Frank R Smith')

	@pytest.mark.django_db
	def test_admin_can_patch_an_employee(self):
		url = reverse('employee-detail', kwargs={'employee_id': 1})

		data = {
			"pay_rate": "8.60"
		}

		response = self.client.patch(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Employee.objects.count(), 3)
		self.assertEqual(response.data['pay_rate'], '8.60')

class TestEmployeeDetailStandardUser(APIUserAPITestCase):
	@pytest.mark.django_db
	def test_standard_user_can_delete_an_employee(self):
		url = reverse('employee-detail', kwargs={'employee_id': 1})

		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	@pytest.mark.django_db
	def test_standard_user_can_update_an_employee(self):
		url = reverse('employee-detail', kwargs={'employee_id': 1})

		data = {
			"name": "Frank R Smith",
			"date_of_hire": timezone.now(),
			"pay_rate": "8.60"
		}

		response = self.client.put(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	@pytest.mark.django_db
	def test_standard_user_can_patch_an_employee(self):
		url = reverse('employee-detail', kwargs={'employee_id': 1})

		data = {
			"pay_rate": "8.60"
		}

		response = self.client.patch(url, data, format='json')

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestPayrollListAnonymous(APITestCase):
	@pytest.mark.django_db
	def test_can_get_payroll_list(self):
		self.client.logout()
		url = reverse('payroll-list', kwargs={'employee_id': 1})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(len(response.data), 1)

class TestPayrollListStandardUser(APIUserAPITestCase):
	@pytest.mark.django_db
	def test_can_get_payroll_list(self):
		url = reverse('payroll-list', kwargs={'employee_id': 1})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(len(response.data), 1)

class TestPayrollListAdmin(APIAdminAPITestCase):
	@pytest.mark.django_db
	def test_can_get_payroll_list(self):
		url = reverse('payroll-list', kwargs={'employee_id': 1})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 4)
"""
class TestPayrollDetailAnonymous(APITestCase):
	@pytest.mark.django_db
	def test_can_get_payroll_detail(self):
		self.client.logout()
		url = reverse('payroll-detail', kwargs={'employee_id': 1, 'payroll_id': 1})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
"""