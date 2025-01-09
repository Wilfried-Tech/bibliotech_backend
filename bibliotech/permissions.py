from rest_framework import permissions


class IsSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(obj == request.user)


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS)


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)

