from rest_framework import permissions


class FoodgramCurrentUserOrAdminOrReadOnly(
        permissions.IsAuthenticatedOrReadOnly):

    def has_permission(self, request, view):
        if (view.action not in ('list', 'retrieve', ) and
                not request.user.is_authenticated):
            return False
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(obj) == type(user) and obj == user:
            return True
        return request.method in permissions.SAFE_METHODS or user.is_admin


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешено чтение для всех, редактирование и удаление только для автора
    и админа.
    """
    def has_permission(self, request, view):
        if (request.user.is_authenticated or
                request.method in permissions.SAFE_METHODS):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated
                    and ((request.user == obj.author)
                         or (request.user.is_admin)))
