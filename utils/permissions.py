from rest_framework import permissions

from society.models import JoinSocietyRequest
from society.constants import JoinSocietyRequestStatus


class IsStudent(permissions.BasePermission):
    message = 'Student Only'

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'student')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class JoinSociety(permissions.BasePermission):
    message = '你已加入该社团'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.student not in obj.members


class SingleJoinSocietyRequestCheck(permissions.BasePermission):
    message = '社长已正在审核你发出的加入请求，请勿重复提交'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return JoinSocietyRequest.objects.filter(
            society=obj,
            member=request.user.student,
            status=JoinSocietyRequestStatus.WAITING
        ).count() == 0


class AccessSocietyAdmin(permissions.BasePermission):
    message = 'Society Only'

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'society')


class AccessSocietyBureauAdmin(permissions.BasePermission):
    message = 'Society Bureau Only'

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'society_bureau')