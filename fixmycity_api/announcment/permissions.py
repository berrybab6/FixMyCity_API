from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSectorAdmin(BasePermission):
    def has_permission(self, request, view):
       return request.user.role == 2
    
   
