from django.contrib import admin

from .models import Follow, User

from users.models import MyToken


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',
                    'password', 'is_active')
    list_filter = ('email', 'username')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')


class MyTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'user')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(MyToken, MyTokenAdmin)
