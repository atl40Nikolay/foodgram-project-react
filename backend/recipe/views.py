from django.db.models import Sum
from django.http import HttpResponse
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph
from rest_framework import decorators, pagination, response, status, viewsets

from rest_framework.permissions import IsAuthenticated

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Recipe, Tag
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Обработка CRUD для рецептов, также для избранного и корзины покупок.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrAdminOrReadOnly, )
    error_messages = {
        'favorite_exists': 'Рецепт `{recipe}` уже есть в избранном.',
        'favorite_is_none': ('Рецепт `{recipe}` уже отсутствует '
                             'в избранном.'),
        'shoping_item_exists': 'Рецепт `{recipe}` уже есть в корзине.',
        'shoping_item_none': 'Рецепт `{recipe}` уже удалён из корзины.',
        'empty_cart': 'Корзина покупок пуста.',

    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @decorators.action(
        detail=True,
        methods=['post', ]
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if not recipe.favorited_recipe.filter(pk=user.id).exists():
            recipe.favorited_recipe.add(user)
            recipe.save()
            serializer = self.get_serializer(
                recipe,
                context={'request': request},
                fields={'id', 'name', 'image', 'cooking_time'},
            )
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return response.Response(
            {'errors': self.error_messages[
                'favorite_exists'].format(recipe=recipe)},
            status=status.HTTP_400_BAD_REQUEST
        )

    @favorite.mapping.delete
    def delete_from_favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if recipe.favorited_recipe.filter(pk=user.id).exists():
            recipe.favorited_recipe.remove(user)
            recipe.save()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
            {'errors': self.error_messages[
                'favorite_is_none'].format(recipe=recipe)},
            status=status.HTTP_400_BAD_REQUEST
        )

    @decorators.action(
        detail=True,
        methods=['post', ]
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if not recipe.in_shoping_cart.filter(pk=user.id).exists():
            recipe.in_shoping_cart.add(user)
            recipe.save()
            serializer = self.get_serializer(
                recipe,
                context={'request': request},
                fields={'id', 'name', 'image', 'cooking_time'},
            )
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return response.Response(
            {'errors': self.error_messages[
                'shoping_item_exists'].format(recipe=recipe)},
            status=status.HTTP_400_BAD_REQUEST
        )

    @shopping_cart.mapping.delete
    def delete_from_shoping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if recipe.in_shoping_cart.filter(pk=user.id).exists():
            recipe.in_shoping_cart.remove(user)
            recipe.save()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
            {'errors': self.error_messages[
                'shoping_item_none'].format(recipe=recipe)},
            status=status.HTTP_400_BAD_REQUEST
        )

    @decorators.action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        recipe_name = 'recipe__name'
        ingredient_name = 'ingredients_for_recipe__ingredient__name'
        measurement_unit = ('ingredients_for_recipe__'
                            'ingredient__measurement_unit')
        amount = 'ingredients_for_recipe__amount'
        filename = 'shopping_list.pdf'
        user = request.user
        recipes = list(
            user.shoping_cart.all().values_list(recipe_name))
        if not recipes:
            return response.Response(
                {'error': self.error_messages['empty_cart']},
                status=status.HTTP_400_BAD_REQUEST
            )
        ingredients_list = list(Recipe.objects
                                .filter(shoping_cart__user=user)
                                .prefetch_related('ingredients')
                                .order_by(ingredient_name)
                                .values_list(ingredient_name,
                                             measurement_unit)
                                .annotate(total=Sum(amount))
                                )
        content = ['Список ингредиентов для {}.\n\n'
                   .format(user.get_full_name())]
        content += ['Теперь вы сможете приготовить следующие блюда:\n']
        content += ['- {}\n'.format(item[0]) for item in recipes]
        content += ['\nСписок требуемых для этого ингредиентов:\n']
        content += ['- {0} - {2} ({1}).\n'.format(*item)
                    for item in ingredients_list]
        pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))
        fileresponse = HttpResponse(content_type='application/pdf')
        fileresponse['Content-Disposition'] = ('attachment; filename={0}'
                                               .format(filename))
        page = canvas.Canvas(fileresponse)
        style = ParagraphStyle('russian_text')
        style.fontName = 'DejaVuSerif'
        style.leading = 0.5 * cm
        for i, part in enumerate(content):
            content[i] = Paragraph(part.replace('\n', '<br></br>'), style)
        frame = Frame(
            0,
            0,
            21 * cm,
            29.7 * cm,
            leftPadding=cm,
            bottomPadding=cm,
            rightPadding=cm,
            topPadding=cm,
        )
        frame.addFromList(content, page)
        page.showPage()
        page.save()
        return fileresponse


class TagsViewSet(viewsets.ModelViewSet):
    """Запросы к tags."""
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly, )


class IngredientsViewSet(viewsets.ModelViewSet):
    """Запросы к ingredients."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', )
