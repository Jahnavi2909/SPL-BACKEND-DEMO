from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"


class IsFranchise(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "FRANCHISE"


from rest_framework.permissions import BasePermission

class IsAdminOrFranchise(BasePermission):

    def has_permission(self, request, view):
        print("HAS_PERMISSION CALLED", request.user, request.user.role)
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'FRANCHISE']

    def has_object_permission(self, request, view, obj):
        print("OBJECT_PERMISSION CALLED", getattr(obj, 'franchise', None), request.user)
        if request.user.role == 'ADMIN':
            return True
        if request.user.role == 'FRANCHISE':
             return hasattr(obj, 'franchise') and obj.franchise.user == request.user

        return False