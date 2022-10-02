from django.contrib.auth import get_user_model

from drf_extra_fields.fields import Base64ImageField
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from rest_framework import serializers as s

from .mixins import DynamicFieldsMixin
from .models import Ingredient, IngredientsAmount, Recipe, Tag
from users.serializers import FoodgramUserSerializer

User = get_user_model()


class TagsSerializer(s.ModelSerializer):
    """Сериализация запросов к tags."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(s.ModelSerializer):
    """Сериализация запросов к ingredients."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(s.ModelSerializer):
    """
    Сериализация запросов к recipes с информацией о количестве продуктов.
    """
    id = s.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = s.CharField(
        read_only=True,
        source='ingredient.name'
    )
    measurement_unit = s.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(DynamicFieldsMixin, s.ModelSerializer):
    """Сериализация запросов к recipes"""
    author = PresentablePrimaryKeyRelatedField(
        presentation_serializer=FoodgramUserSerializer,
        read_source=None,
        read_only=True
    )
    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredients_for_recipe',
    )
    tags = PresentablePrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        presentation_serializer=TagsSerializer,
        many=True,
        read_source=None
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True,
    )
    is_favorited = s.SerializerMethodField()
    is_in_shoping_cart = s.SerializerMethodField()

    default_error_messages = {
        'incorrect_type': ('Некорректный тип {input_obj}. Ожидается '
                           '{input_expected}, в запросе {input_type}.'),
        'empty_list': 'Поле {input_obj} не может быть пустым.',
        'unique_item': ('Значения {input_obj} должны быть уникальными '
                        'для одного рецепта.'),
    }

    class Meta:
        model = Recipe
        depth = 1
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shoping_cart', 'name', 'image', 'text',
                  'cooking_time']

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.favorited_recipe.filter(pk=user.id).exists()
        # return FavoriteRecipes.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shoping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.in_shoping_cart.filter(pk=user.id).exists()

    def validate(self, attrs):
        ingredients_data = self.initial_data.get('ingredients')
        tags_data = self.initial_data.get('tags')
        if type(ingredients_data) not in (list, tuple):
            self.fail(
                'incorrect_type',
                input_type=type(ingredients_data).__name__,
                input_expected='list',
                input_obj='ingredients'
            )
        if len(ingredients_data) == 0:
            self.fail(
                'empty_list',
                input_obj='ingredients'
            )
        ingredients_data = [ing['id'] for ing in ingredients_data]
        if len(ingredients_data) != len(set(ingredients_data)):
            self.fail(
                'unique_item',
                input_obj='ingredients'
            )
        if type(tags_data) not in (list, tuple):
            self.fail(
                'incorrect_type',
                input_type=type(tags_data).__name__,
                input_expected='list',
                input_obj='tags'
            )
        if len(tags_data) != len(set(tags_data)):
            self.fail(
                'unique_item',
                input_obj='tags'
            )
        return super().validate(attrs)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients_for_recipe')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            **validated_data
        )
        recipe.tags.set(tags)
        for ingredient_data in ingredients:
            ingredient = ingredient_data['ingredient']['id']
            amount = ingredient_data['amount']
            IngredientsAmount.objects.get_or_create(
                ingredient=ingredient,
                recipe=recipe,
                amount=amount)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name', instance.name
        )
        instance.image = validated_data.get(
            'image', instance.image
        )
        instance.text = validated_data.get(
            'text', instance.text
        )
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags = validated_data.get('tags')
        instance.tags.set(tags)
        instance.ingredients.clear()
        ingredients = validated_data.get('ingredients_for_recipe')
        for ingredient_data in ingredients:
            IngredientsAmount.objects.get_or_create(
                ingredient=ingredient_data['ingredient']['id'],
                amount=ingredient_data['amount'],
                recipe=instance
            )
        instance.save()
        return instance
