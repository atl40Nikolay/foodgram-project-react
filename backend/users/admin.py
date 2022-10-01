from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',
                    'password', 'is_active')
    list_filter = ('email', 'username')


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
