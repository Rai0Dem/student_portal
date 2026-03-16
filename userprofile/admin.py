from django.contrib import admin
from django.utils.html import format_html
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'gender', 'birthdate', 'avatar_thumbnail')
    search_fields = ('user__username', 'user__email')
    list_filter = ('role' ,'gender')

    readonly_fields = ('avatar_thumbnail',)

    fieldsets = (
        ('User Info', {
            'fields': ('user', 'role')
        }),
        ('Personal Details', {
            'fields': ('birthdate', 'gender', 'bio')
        }),
        ('Profile Image', {
            'fields': ('avatar', 'avatar_thumbnail')
        }),
    )

    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="70" style="border-radius: 8px;" />',
                obj.avatar.url
            )
        return "No Avatar"

    avatar_thumbnail.short_description = "Preview"
