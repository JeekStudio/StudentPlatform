from rest_framework import permissions

from society.models import JoinSocietyRequest
from society.constants import JoinSocietyRequestStatus, ActivityRequestStatus, SocietyStatus


class IsStudent(permissions.BasePermission):
    message = 'Student Only'

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'student')


class IsStudentSelf(IsStudent):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class JoinSociety(permissions.BasePermission):
    message = '你已加入该社团'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.student not in obj.members.all()


class QuitSociety(permissions.BasePermission):
    message = '你未加入该社团，无法退出'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.student in obj.members.all()


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


class IsSociety(permissions.BasePermission):
    message = 'Society Only'

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'society')


class IsSocietyBureau(permissions.BasePermission):
    message = 'Society Bureau Only'

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'society_bureau')


# Only unconfirmed activities are allowed to be edited.
class SocietyActivityEditable(permissions.BasePermission):
    message = 'Not Allowed To Edit'

    def has_object_permission(self, request, view, obj):
        if request.method != 'PATCH' and request.method != 'PUT':
            return True
        return obj.status == ActivityRequestStatus.WAITING


class SocietyIsWaiting(permissions.BasePermission):
    message = 'Only Waiting Society Allowed'

    def has_object_permission(self, request, view, obj):
        return obj.status == SocietyStatus.WAITING


class SocietyIsActive(permissions.BasePermission):
    message = 'Only Active Society Allowed'

    def has_object_permission(self, request, view, obj):
        return obj.status == SocietyStatus.ACTIVE


class SocietyIsArchived(permissions.BasePermission):
    message = 'Only Archived Society Allowed'

    def has_object_permission(self, request, view, obj):
        return obj.status == SocietyStatus.ARCHIVED
