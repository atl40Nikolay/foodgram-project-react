DEFAULT_ERROR_MESSAGES = {
    'incorrect_type': ('Некорректный тип {input_obj}. Ожидается '
                       '{input_expected}, в запросе {input_type}.'),
    'empty': 'Поле {input_obj} не может быть пустым.',
    'unique': ('Значения {input_obj} должны быть уникальными '
               'для одного рецепта.'),
    'is_self_post': 'Дорогой {user}, подписка на себя самого невозможна.',
    'is_self_delete': ('Отписка от самого себя не должна была случиться, '
                       'но если это произошло, знайте - это невозможно.'),
    'unique_subscription_post': 'Вы ({user}) уже подписаны на {author}.',
    'false_subscription_delete': 'Вы ({user}) уже отписаны от {author}.',
    'incorrect_query': ('Ошибка в query-параметрах: {query}. '
                        'Некорректный параметр `limit`: {limit}.'),
}
