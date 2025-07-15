from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'avatar', 'user_email')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    list_per_page = 20
    fields = ('user', 'role', 'avatar')
    readonly_fields = ('user',)
    list_editable = ('role',)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    fields = ('role', 'avatar')
    readonly_fields = ('role',)

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_per_page = 20
    inlines = (UserProfileInline,)
    ordering = ('-date_joined',)