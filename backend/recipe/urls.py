from django.urls import include, path

from foodgram.core.routers import StandartRouter
from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet

app_name = 'recipe'


router = StandartRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
]
