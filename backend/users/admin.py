from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from .models import Follow, User, MyToken


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',
                    'is_active', 'password', )
    search_fields = ('email', 'username', )
    list_filter = ('email', 'username', 'is_superuser', 'is_staff', )


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', )
    search_fields = (
        '^user__email',
        '^user__username',
        '^author__email',
        '^author__username',
    )


class MyTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created', )


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(MyToken, MyTokenAdmin)
