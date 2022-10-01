from rest_framework import permissions


class FoodgramCurrentUserOrAdminOrReadOnly(
        permissions.IsAuthenticatedOrReadOnly):
    """
    Пермишн для проверки доступа пользователей к спискам пользователей.
    """
    def has_permission(self, request, view):
        if (view.action not in ('list', 'retrieve', )
                and not request.user.is_authenticated):
            return False
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(obj) == type(user) and obj == user:
            return True
        return request.method in permissions.SAFE_METHODS or user.is_admin
