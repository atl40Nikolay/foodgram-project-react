from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import SimpleRouter


class StandartRouter(SimpleRouter):
    """Обход проблемы Append Slash."""
    def __init__(self, trailing_slash='/?'):
        super(StandartRouter, self).__init__()
        self.trailing_slash = trailing_slash


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls', namespace='users')),
    path('api/', include('recipe.urls', namespace='recipe')),
]
