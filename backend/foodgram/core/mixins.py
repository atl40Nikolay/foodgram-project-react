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
