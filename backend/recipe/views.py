from django.db.models import Sum
from django.http import HttpResponse
from django_filters import rest_framework as filters

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, Paragraph
from rest_framework import decorators, pagination, response, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from . import conf
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
            {'errors': conf.ERROR_MESSAGES[
                'favorite_exists'].format(recipe=recipe)},
            status=status.HTTP_400_BAD_REQUEST
        )

    @favorite.mapping.delete
    def delete_from_favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if recipe.favorited_recipe.filter(pk=user.id).exists():
            recipe.favorited_recipe.remove(user)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
            {'errors': conf.ERROR_MESSAGES[
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
            {'errors': conf.ERROR_MESSAGES[
                'shoping_item_exists'].format(recipe=recipe)},
            status=status.HTTP_400_BAD_REQUEST
        )

    @shopping_cart.mapping.delete
    def delete_from_shoping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if recipe.in_shoping_cart.filter(pk=user.id).exists():
            recipe.in_shoping_cart.remove(user)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
            {'errors': conf.ERROR_MESSAGES[
                'shoping_item_none'].format(recipe=recipe)},
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
            user.shoping_cart.all().values_list(conf.RECIPE_NAME))
        if not recipes:
            return response.Response(
                {'error': conf.ERROR_MESSAGES['empty_cart']},
                status=status.HTTP_400_BAD_REQUEST
            )
        ingredients_list = list(Recipe.objects
                                .filter(shoping_cart__user=user)
                                .prefetch_related('ingredients')
                                .order_by(conf.INGREDIENT_NAME)
                                .values_list(conf.INGREDIENT_NAME,
                                             conf.MEASUREMENT_UNIT)
                                .annotate(total=Sum(conf.AMOUNT))
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
                                               .format(conf.FILENAME))
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
