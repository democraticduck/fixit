from django.contrib import admin
from django.utils import timezone
from .models import Notification, Report, User

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'approve_status', 'case_status', 'created_at', 'days_since_creation',)
    list_filter = ('category', 'approve_status', 'case_status', )
    search_fields = ('title',)
    fields = ('title', 'description', 'loc_lng', 'loc_lat', 'approve_status', 'category', 'photo_url', 'created_at', 'updated_at', 'user_id', 'manage_by', 'case_status', 'progress_detail',)
    readonly_fields = ('title', 'description', 'loc_lng', 'loc_lat', 'category', 'photo_url', 'created_at', 'updated_at', 'user_id', 'case_status', 'progress_detail',)

    def save_model(self, request, obj, form, change):
        if change:
            report = Report.objects.get(pk=obj.pk)

            # Notify user if approval status changed to approved
            if report.approve_status != obj.approve_status:
                if obj.approve_status == 'ap':
                    Notification.objects.create(
                        title=f"Approved: {report.title}",
                        description=f"Your report has been approved by the admin.",
                        sent_at=timezone.now(),
                        report=obj
                    )

                elif obj.approve_status == 'rj':
                    obj.case_status = 'cl'
                    Notification.objects.create(
                        title=f"Rejected: {report.title}",
                        description=f"Your report has been rejected by the admin.",
                        sent_at=timezone.now(),
                        report=obj
                    )

            if report.manage_by != obj.manage_by and obj.manage_by is not None:
                obj.case_status = 'op'
                Notification.objects.create(
                    title=f"New: {report.title}",
                    description=f"You have been assigned to manage the case: \"{obj.title}\".",
                    sent_at=timezone.now(),
                    report=obj
                )

        super().save_model(request, obj, form, change)


class UserAdmin(admin.ModelAdmin):
    list_display = ('ic_num', 'first_name', 'last_name', 'phone_num', 'role',)
    list_filter = ('role',)
    search_fields = ('ic_num',)

admin.site.register(Report, ReportAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Notification)
