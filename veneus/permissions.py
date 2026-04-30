from rest_framework.permissions import BasePermission, SAFE_METHODS
 
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Public can read
        if request.method in SAFE_METHODS:
            return True
       
        # Only admin can create/update/delete
        return request.user and request.user.is_staff