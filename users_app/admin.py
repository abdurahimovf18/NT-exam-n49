from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


UserModel = get_user_model()


admin.site.unregister(Group)


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ("pk", "full_name", "created_at", "updated_at")
    search_fields = ("pk", "first_name", "last_name", "created_at")
    list_display_links = ("full_name", )
