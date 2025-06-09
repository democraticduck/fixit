from django.contrib import admin
from .models import Report, Notification
from .models import User
from django.utils import timezone

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_at', 'days_since_creation')
    list_filter = ('status', 'category', )
    search_fields = ('title', )

    fields = ('title', 'description', 'loc_lng', 'loc_lat', 'status', 'category', 'photo_url', 'user_id',)

    readonly_fields = ('title', 'description', 'loc_lng', 'loc_lat', 'category', 'photo_url', 'user_id',)
    @property
    def days_since_creation(self):
        diff = timezone.now() - self.created_at
        return diff.days

class UserAdmin(admin.ModelAdmin):
    list_display = ('ic_num', 'phone_num',)
    search_fields = ('ic_num', )

admin.site.register(Report, ReportAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Notification)