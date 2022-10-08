from django.core import validators
from django.db import models

from colorfield.fields import ColorField


class Tag(models.Model):
    TAG_MAX_NAMES_LENGTH = 200
    COLORS = (
        ('R', '#FF0000'),
        ('O', '#FFA500'),
        ('Y', '#FFFF00'),
        ('G', '#008000'),
        ('C', '#00FFFF'),
        ('B', '#0000FF'),
        ('P', '#800080'),
        ('Bl', '#000000'),
    )
    name = models.CharField(
        'название тэга',
        unique=True,
        max_length=TAG_MAX_NAMES_LENGTH,
        help_text='Название.',
    )
    color = ColorField(
        'цвет тэга',
        unique=True,
        samples=COLORS,
        help_text='Цвет тэга.',
    )
    slug = models.SlugField(
        'уникальный слаг',
        unique=True,
        max_length=TAG_MAX_NAMES_LENGTH,
        help_text='Машинное имя.',
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    INGREDIENT_MAX_NAME_LENGTH = 200
    MEASUREMENT_UNIT_MAX_LENGTH = 200
    name = models.CharField(
        'название ингредиента',
        max_length=INGREDIENT_MAX_NAME_LENGTH,
        help_text='Название ингредиента.',
    )
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=MEASUREMENT_UNIT_MAX_LENGTH,
        help_text='Единица измерения.',
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='ingredients_with_measurement_unit_unique_constraint'
            ),
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    MIN_COOKING_TIME = 1
    RECIPE_MAX_NAME_LENGTH = 200
    RECIPE_MAX_TEXT_LENGTH = 500
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='автор рецепта',
        related_name='user_recipes',
        help_text='Автор рецепта.',

    )
    name = models.CharField(
        'название рецепта',
        unique=True,
        max_length=RECIPE_MAX_NAME_LENGTH,
        help_text='Название рецепта.',
    )
    image = models.ImageField(
        'изображение: ммм нямка!',
        help_text='Изображение: ммм нямка!',
    )
    text = models.TextField(
        'описание рецепта',
        max_length=RECIPE_MAX_TEXT_LENGTH,
        help_text='Описание рецепта.',
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through='IngredientsAmount',
        related_name='recipes_with_ingredient',
        verbose_name='ингредиенты',
        help_text='Ингредиенты рецепта.',
    )
    favorited_recipe = models.ManyToManyField(
        to='users.User',
        through='FavoriteRecipes',
        related_name='favorited_recipes',
        verbose_name='рецепты в избранном',
        help_text='Рецепты в избранном.',
    )
    in_shopping_cart = models.ManyToManyField(
        to='users.User',
        through='ShopingCart',
        related_name='shopping_recipes',
        verbose_name='рецепты в корзине',
        help_text='Рецепты в корзине.',
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='тэги',
        help_text='Тэги.',
    )
    cooking_time = models.PositiveIntegerField(
        'время приготовления (в минутах)',
        validators=[
            validators.MinValueValidator(
                MIN_COOKING_TIME,
                'Время приготовления не может быть меньше чем {} мин.'
                .format(MIN_COOKING_TIME)
            )
        ],
        help_text='Время приготовления рецепта(мин).',
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True,
        help_text='Дата публикации рецепта.',
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class IngredientsAmount(models.Model):
    MIN_AMOUNT = 1
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='название ингредиента',
        related_name='ingredients_for_recipe',
        help_text='Название ингредиента из рецепта.',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='название рецепта',
        related_name='ingredients_for_recipe',
        help_text='Название рецепта',
    )
    amount = models.PositiveIntegerField(
        'количество продукта',
        default=MIN_AMOUNT,
        validators=[validators.MinValueValidator(MIN_AMOUNT)],
        help_text='Количество.',
    )

    class Meta:
        verbose_name = 'ингредиент для рецепта'
        verbose_name_plural = 'ингредиенты для рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='ingredients_in_recipe_unique_constraint'
            ),
        ]

    def __str__(self):
        return (f'Ингредиент для рецепта {self.recipe}: '
                f'{self.ingredient} - {self.amount} '
                f'({self.ingredient.measurement_unit})')


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='пользователь',
        help_text='Владелец избранного.',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='рецепт в избранном',
        help_text='Рецепт в избранном.',
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'много МНОГО избранных'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='users_favorite_recipe_unique_constraint'
            ),
        ]

    def __str__(self):
        return f'Рецепт `{self.recipe}` в избранном у {self.user}'


class ShopingCart(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='покупатель',
        help_text='Владелец корзины.',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='покупки',
        help_text='Рецепт в корзине.',
    )

    class Meta:
        verbose_name = 'корзина для покупок'
        verbose_name_plural = 'корзины для покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='recipes_in_shopingcart_unique_constraint'
            ),
        ]

    def __str__(self):
        return f'Рецепт `{self.recipe}` в корзине у {self.user}'
