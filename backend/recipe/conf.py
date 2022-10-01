CONSTRAINT_VALUES = {
    'MIN_COOKING_TIME': 1,
    'MIN_AMOUNT': 1,
    'MAX_NAMES_LENGTH': 200,
    'MAX_TEXT_LENGTH': 500,
}


ERROR_MESSAGES = {
    'favorite_exists': 'Рецепт `{recipe}` уже есть в избранном.',
    'favorite_is_none': ('Рецепт `{recipe}` уже отсутствует '
                         'в избранном.'),
    'shoping_item_exists': 'Рецепт `{recipe}` уже есть в корзине.',
    'shoping_item_none': 'Рецепт `{recipe}` уже удалён из корзины.',
    'incorrect_type': ('Некорректный тип {input_obj}. Ожидается '
                       '{input_expected}, в запросе {input_type}.'),
    'empty': 'Поле {input_obj} не может быть пустым.',
    'empty_cart': 'Корзина покупок пуста.',
    'unique': ('Значения {input_obj} должны быть уникальными '
               'для одного рецепта.'),
}

# Эти константы лишь для удобочитаемости кода, а вот куда их праильно
# спрятать - в модели вроде нелогично т.к. нужны только во вьюхе, в
# сериализатор по той же причине не убираю, а какие ещё варианты?
RECIPE_NAME = 'recipe__name'

INGREDIENT_NAME = 'ingredients_for_recipe__ingredient__name'

MEASUREMENT_UNIT = 'ingredients_for_recipe__ingredient__measurement_unit'

AMOUNT = 'ingredients_for_recipe__amount'

FILENAME = 'shopping_list.pdf'
