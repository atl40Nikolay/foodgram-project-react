from django.contrib import admin

from models import User, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',
                    'password', 'is_active')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class FavoritRecipesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
