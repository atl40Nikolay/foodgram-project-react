from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from djoser.serializers import UserCreateSerializer, UserSerializer

from rest_framework import serializers as s
from rest_framework.validators import UniqueValidator

from models import Follow

User = get_user_model()


class FoodgramUserSerializer(UserSerializer):
    """ """
    is_subscribed = s.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.follows.filter(
            user__pk=user.id,
            author__pk=obj.id).exists()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')


class FollowsSerializer(FoodgramUserSerializer):
    """ """
    recipes = s.SerializerMethodField()
    recipes_count = s.SerializerMethodField('get_recipescount')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipescount(self, obj):
        return obj.user_recipes.count()

    def get_recipes(self, obj):
        from recipe.serializers import RecipeSerializer
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = obj.user_recipes.all()
        if limit is not None:
            limit = abs(int(limit))
            queryset = queryset[:limit]
        return RecipeSerializer(
                queryset,
                context={'request': request},
                fields={'id', 'name', 'image', 'cooking_time'},
                many=True
            ).data


class FoodgramUserCreateSerializer(UserCreateSerializer):

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
