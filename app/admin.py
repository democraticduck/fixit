from django.contrib import admin
from .models import Notification, Report, User

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'approve_status', 'created_at', 'days_since_creation')
    list_filter = ('approve_status', 'category')

    search_fields = ('title',)

    fields = ('title', 'description', 'loc_lng', 'loc_lat', 'approve_status', 'category', 'photo_url', 'created_at', 'updated_at', 'user_id', 'manage_by', 'case_status', 'progress_detail')
    readonly_fields = ('title', 'description', 'loc_lng', 'loc_lat', 'category', 'photo_url', 'created_at', 'updated_at', 'user_id', 'case_status', 'progress_detail')


class UserAdmin(admin.ModelAdmin):
    list_display = ('ic_num', 'first_name', 'last_name', 'phone_num', 'role')
    list_filter = ('role',)
    
    search_fields = ('ic_num',)


admin.site.register(Report, ReportAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Notification)
