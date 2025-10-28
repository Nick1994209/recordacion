from django.contrib import admin
from .models import RecordEntry, RecordImage


class RecordImageInline(admin.TabularInline):
    """Inline admin for RecordImage to manage images within RecordEntry"""
    model = RecordEntry.images.through
    extra = 1
    verbose_name = "Картинка"
    verbose_name_plural = "Картинки"


@admin.register(RecordEntry)
class RecordEntryAdmin(admin.ModelAdmin):
    """Admin configuration for RecordEntry model"""
    list_display = ('title', 'is_approved', 'approved_by', 'created_at', 'updated_at')
    list_filter = ('is_approved', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'preview_image')
        }),
        ('Статус', {
            'fields': ('is_approved', 'approved_by')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [RecordImageInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('approved_by')


@admin.register(RecordImage)
class RecordImageAdmin(admin.ModelAdmin):
    """Admin configuration for RecordImage model"""
    list_display = ('id', 'image', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    list_filter = ('uploaded_at',)
