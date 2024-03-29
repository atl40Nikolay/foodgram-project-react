from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers as s
from rest_framework.validators import UniqueValidator

from recipe.mixins import GetRecipesFromQueryMixin

User = get_user_model()


class FoodgramUserSerializer(UserSerializer):
    """Сериализация обьекта пользователя при запросе к users."""
    is_subscribed = s.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.follows.filter(
                id=obj.id).exists()
        return False

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')


class FollowsSerializer(
    GetRecipesFromQueryMixin,
    FoodgramUserSerializer
):
    """Сериализация обьектов пользователей при запросе subscriptions."""
    recipes = s.SerializerMethodField()
    recipes_count = s.SerializerMethodField('get_recipescount')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipescount(self, obj):
        return obj.user_recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = obj.user_recipes.all()
        if limit is not None:
            limit = abs(int(limit))
            queryset = queryset[:limit]
        return self.get_recipes_from_query(queryset, request)


class FoodgramUserCreateSerializer(UserCreateSerializer):
    """Десериализация обьекта пользователя при запросе к users."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'password', 'first_name',
                  'last_name')
        extra_kwargs = {
            'username': {
                'min_length': 2,
                'max_length': 150,
                'validators': [UniqueValidator(
                    queryset=User.objects.all()),
                    UnicodeUsernameValidator()
                ],
                'required': True,
            },
            'email': {
                'max_length': 254,
                'validators': [UniqueValidator(
                    queryset=User.objects.all()),
                    UnicodeUsernameValidator()
                ],
                'required': True,
            },
            'password': {
                'required': True,
            },
            'first_name': {
                'required': True,
            },
            'last_name': {
                'required': True,
            }

        }
