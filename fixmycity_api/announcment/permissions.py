from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSectorAdmin(BasePermission):
    def has_permission(self, request, view):
       print("role is ", request.user.role)
       return request.user.role == 2
   
   

class IsCustomUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 3
    
    
class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 1
    
    
   
