from django.contrib import admin

from .models import (FavoriteRecipes, Ingredient, IngredientsAmount,
                     Recipe, ShopingCart, Tag)


class IngredientsAmountInline(admin.TabularInline):
    model = IngredientsAmount
    extra = 1


class FavoriteRecipesInline(admin.TabularInline):
    model = FavoriteRecipes
    extra = 1


class ShopingCartInline(admin.TabularInline):
    model = ShopingCart
    extra = 1


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug', )
    empty_value_display = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )
    search_fields = ('name', )
    list_filter = ('name',)
    list_max_show_all = 100
    empty_value_display = "-пусто-"


class IngredientsAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount', )
    list_filter = ('recipe__name', 'ingredient__name', )
    empty_value_display = "-пусто-"


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'count_favorites', )
    list_filter = ('author', 'name', 'tags', )
    search_fields = ('name', '^author__email', '^author__username', )
    empty_value_display = "-пусто-"
    readonly_fields = ('count_favorites', )
    inlines = [
        IngredientsAmountInline,
        FavoriteRecipesInline,
        ShopingCartInline,
    ]

    def count_favorites(self, obj):
        return obj.favorite_recipes.count()


class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    search_fields = ('name', '^user__email', '^user__username', )
    list_filter = ('recipe__tags', )


class ShopingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    search_fields = ('name', '^user__email', '^user__username', )
    list_filter = ('recipe__tags', )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientsAmount, IngredientsAmountAdmin)
admin.site.register(FavoriteRecipes, FavoriteRecipesAdmin)
admin.site.register(ShopingCart, ShopingCartAdmin)
