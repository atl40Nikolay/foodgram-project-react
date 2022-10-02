from django.contrib import admin

from .models import (FavoriteRecipes, Ingredient, IngredientsAmount,
                     Recipe, ShopingCart, Tag)


class IngredientsInline(admin.TabularInline):
    model = IngredientsAmount
    extra = 1


class TagAdmin(admin.ModelAdmin):
    empty_value_display = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name', )
    list_max_show_all = 100
    empty_value_display = "-пусто-"


class IngredientsAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe')
    empty_value_display = "-пусто-"
    inlines = [IngredientsInline, ]


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', )
    empty_value_display = "-пусто-"
    readonly_fields = ('count_favorites', )
    inlines = [IngredientsInline, ]

    def count_favorites(self, obj):
        return obj.favorite_recipes.count()


class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


class ShopingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientsAmount)
admin.site.register(FavoriteRecipes, FavoriteRecipesAdmin)
admin.site.register(ShopingCart, ShopingCartAdmin)
