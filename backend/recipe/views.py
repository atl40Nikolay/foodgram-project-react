from django.db.models import Sum
from django.http import HttpResponse
from django_filters import rest_framework as filters

from rest_framework import decorators, response, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from core.filters import IngredientFilter, RecipeFilter
from core.permissions import IsAuthorOrAdminOrReadOnly
from models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeSerializer, TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    _RECIPE_NAME = 'recipe__name'
    _INGREDIENT_NAME = 'ingredients_for_recipe__ingredient__name'
    _MEASUREMENT_UNIT = 'ingredients_for_recipe__ingredient__measurement_unit'
    _AMOUNT = 'ingredients_for_recipe__amount'
    _FILENAME = 'shopping_list.txt'
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrAdminOrReadOnly, )

    @decorators.action(
        detail=True,
        methods=['post', ]
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if recipe.favorited_recipe.filter(pk=user.id).exists():
            return response.Response(
                {'errors': 'Рецепт `{}` уже есть в избранном.'.format(recipe)},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RecipeSerializer(
            recipe,
            context={'request': request},
            fields={'id', 'name', 'image', 'cooking_time'},

        )
        recipe.favorited_recipe.add(user)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @favorite.mapping.delete
    def delete_from_favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if recipe.favorited_recipe.filter(pk=user.id).exists():
            recipe.favorited_recipe.remove(user)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
                {'errors': 'Этого рецепта ещё (или уже) нет в избранном.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @decorators.action(
        detail=True,
        methods=['post', ]
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if recipe.in_shoping_cart.filter(pk=user.id).exists():
            return response.Response(
                {'errors': 'Рецепт `{}` уже есть в корзине.'.format(recipe)},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RecipeSerializer(
            recipe,
            context={'request': request},
            fields={'id', 'name', 'image', 'cooking_time'}
        )
        recipe.in_shoping_cart.add(user)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @shopping_cart.mapping.delete
    def delete_from_shoping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if recipe.in_shoping_cart.filter(pk=user.id).exists():
            recipe.in_shoping_cart.remove(user)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
                {'errors': 'Этого рецепта ещё (или уже) нет в корзине.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @decorators.action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """"""
        user = request.user
        recipes = list(
            user.shoping_cart.all().values_list(self._RECIPE_NAME))
        if not recipes:
            return response.Response(
                {'error': 'Корзина покупок пуста.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ingredients_list = list(Recipe.objects
                                .filter(shoping_cart__user=user)
                                .prefetch_related('ingredients')
                                .order_by(self._INGREDIENT_NAME)
                                .values_list(self._INGREDIENT_NAME,
                                             self._MEASUREMENT_UNIT)
                                .annotate(total=Sum(self._AMOUNT))
                                )
        content = ['Список ингредиентов для {}.\n\n'
                   .format(user.get_full_name())]
        content += ['Теперь вы сможете приготовить следующие блюда:\n']
        content += ['- {}\n'.format(item[0]) for item in recipes]
        content += ['\nСписок требуемых для этого ингредиентов:\n']
        content += ['- {0} - {2} ({1}).\n'.format(*item)
                    for item in ingredients_list]

        fileresponse = HttpResponse(
            content,
            content_type='text/plain,charset=utf8')
        fileresponse['Content-Disposition'] = ('attachment; filename={0}'
                                               .format(self._FILENAME))
        return fileresponse


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', )
