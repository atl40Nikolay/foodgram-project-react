from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Пермишн для доступа к тэгам и ингредиентам. Разрешено
    чтение для всех, создание, редаетирование и удаление
    только для уникальных белых снежинок.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Пермишн для доступа к рецептам. Разрешено чтение для всех,
    редактирование и удаление только для автора и админа.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and ((request.user == obj.author)
                     or (request.user.is_admin)))
