# from django.shortcuts import get_object_or_404
# from rest_framework import response
from rest_framework import serializers

from recipe.models import Recipe


class DynamicFieldsMixin:
    """
    ModelSerializer принимает дополнительный аргумент `fields`
    позволяющий выбрать какие поля вместо дефолтных выводить.
    Украдено с https://www.django-rest-framework.org/ :-/
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class GetRecipesFromQueryMixin:
    """
    В дальнейшем хотелось бы расширить и углубить
    функционал до возможости выдавать репрезентацию
    импортируемого сериалайзера с произвольным набором
    полей, но пока не успеваю :-/
    """
    class RecipeShortReadOutSerializer(
        DynamicFieldsMixin,
        serializers.ModelSerializer
    ):
        class Meta:
            model = Recipe
            fields = ('id', 'name', 'image', 'cooking_time')

    def get_recipes_from_query(self, queryset, request, fields=None):
        kwargs = {
            'context': {'request': request},
            'many': True
        }
        if fields is not None:
            kwargs['fields'] = fields
        serializer = self.RecipeShortReadOutSerializer(
            queryset,
            **kwargs
        )
        return serializer.data
