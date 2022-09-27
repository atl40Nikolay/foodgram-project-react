from django.urls import include, path

from foodgram.core.routers import StandartRouter
from .views import FoodgramUserViewSet

app_name = 'users'

router = StandartRouter()
router.register('users', FoodgramUserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]
