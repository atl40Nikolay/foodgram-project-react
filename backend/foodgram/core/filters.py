from django.contrib.auth import get_user_model

from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from recipe.models import Recipe, Tag

User = get_user_model()


class IngredientFilter(SearchFilter):
    """
    Фильтр для поиска ингредиента по имени.
    С перспективой дальнейшего апгрейда.
    """
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    """
    Фильтр для сортировки по тэгам, поиска по автору, сортировки
    по наличию в корзине или в избранном.
    """
    tags = filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart', method='filter'
    )
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited', method='filter'
    )

    def filter(self, queryset, name, value):
        if not self.request.user.is_authenticated:
            return queryset
        if name == 'is_in_shopping_cart':
            if value is True:
                queryset = queryset.filter(
                    shoping_cart__user=self.request.user
                )
            else:
                queryset = queryset.exclude(
                    shoping_cart__user=self.request.user
                )
        elif name == 'is_favorited':
            if value is True:
                queryset = queryset.filter(
                    favorite_recipes__user=self.request.user
                )
            else:
                queryset = queryset.exclude(
                    favorite_recipes__user=self.request.user
                )
        else:
            return queryset  # Ошибка flake R503 либо
        return queryset  # Ошибка flake R504, видимо некорректная?

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)
