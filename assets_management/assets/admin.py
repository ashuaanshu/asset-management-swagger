from django.contrib import admin

from .models import Assets, Violation, Notification

@admin.register(Assets)

class AdminAssets(admin.ModelAdmin):
    list_display= ('name', 'service_time', 'expire_time', 'is_serviced', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_serviced',)

@admin.register(Notification)

class AdminNotification(admin.ModelAdmin):
    list_display = ('assets', 'notification_type', 'messages', 'created_at')
    search_fields = ('assets__name', 'notification_type')

@admin.register(Violation)

class AdminViolation(admin.ModelAdmin):
    list_display = ('assets', 'violation_type', 'messages', 'created_at')
    search_fields = ('assets__name', 'violation_type')