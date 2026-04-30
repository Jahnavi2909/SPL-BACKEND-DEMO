from rest_framework.permissions import BasePermission, SAFE_METHODS
 
 
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True   # GET for all
        return request.user.is_staff   # Only admin can modify