from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not obj.groups.exists():
            group = Group.objects.get(name='Usuario')
            obj.groups.add(group)

        if 'admin' in request.user.username.lower():
            group = Group.objects.get(name='Trabajador')
            obj.groups.add(group)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
