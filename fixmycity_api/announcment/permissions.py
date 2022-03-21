from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSectorAdmin(BasePermission):
    
    def has_permission(self, request, view):
        print(request.user.is_authenticated)
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        print(obj)
        print(request.user)
        
        return obj == request.user
