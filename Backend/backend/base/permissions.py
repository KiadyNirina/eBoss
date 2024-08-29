from rest_framework.permissions import BasePermission

class IsSchoolUser(BasePermission) :
    def has_permission(self, request, view):
        return request.user and request.user.role == 'school'
    
class IsStudentUser(BasePermission) :
    def has_permission(self, request, view):
        return request.user and request.user.role == 'student'