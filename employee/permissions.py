from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrOwner(BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in SAFE_METHODS and obj.employee == request.user:
			return True

		return request.user.is_staff

