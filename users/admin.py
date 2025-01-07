from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_staff', 'is_active', 'last_login', 'date_joined']
    readonly_fields = ['groups', 'date_joined', 'user_permissions', 'last_login', 'password']
    search_fields = ['username', 'email']
    list_filter = ['is_active', 'is_staff']
    ordering = ['id']
    fieldsets = [
        (None, {'fields': ['username', 'email', 'password']}),
        ('Permissions', {'fields': ['is_active', 'is_staff', 'is_superuser']}),
        ('Date Importantes', {'fields': ['last_login', 'date_joined']}),
        ('Groupes', {'fields': ['groups']}),
        ('Permissions D\'utilisateur', {'fields': ['user_permissions']}),
    ]

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=...):
        if request.user == obj:
            return self.readonly_fields + ['is_active']
        allowed_fields = ['is_staff', 'is_superuser', 'is_active']
        return [f.name for f in User._meta.get_fields() if f.name not in allowed_fields]

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.save()
