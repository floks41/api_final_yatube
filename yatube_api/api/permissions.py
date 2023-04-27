"""Модуль разрешений для представлений приложения Api."""


from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Небезопасные методы HTTP разрешены только автору.

    В остальные случаях разрешены безопасные методы HTTP: GET, HEAD, OPTIONS.
    """
    def has_object_permission(self, request, view, obj):
        """Ограничение на уровне объекта."""
        return request.method in SAFE_METHODS or obj.author == request.user
