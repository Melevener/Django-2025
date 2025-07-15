from django.contrib import admin
from .models import Articles

@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'anons', 'date', 'id')
    list_filter = ('date',)
    search_fields = ('title', 'anons', 'full_text')
    date_hierarchy = 'date'
    list_per_page = 20
    fields = ('title', 'anons', 'full_text', 'date')
    readonly_fields = ('date',)
    list_editable = ('anons',)
    ordering = ('-date',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()