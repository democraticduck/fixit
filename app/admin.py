from django.contrib import admin
from django.utils import timezone
from .models import Notification, Report, User, RegistrationRequest

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'approve_status', 'case_status', 'created_at', 'days_since_creation',)
    list_filter = ('category', 'approve_status', 'case_status', )
    search_fields = ('title',)
    fields = ('title', 'description', 'loc_lng', 'loc_lat', 'approve_status', 'category', 'photo_url', 'created_at', 'updated_at', 'user_id', 'manage_by', 'case_status', 'progress_detail',)
    readonly_fields = ('title', 'description', 'loc_lng', 'loc_lat', 'category', 'photo_url', 'created_at', 'updated_at', 'user_id', 'case_status', 'progress_detail',)

    def save_model(self, request, obj, form, change):
        if change:
            previous = Report.objects.get(pk=obj.pk)

            if previous.approve_status != obj.approve_status and obj.approve_status == Report.APPROVE_STATUS.REJECTED:
                obj.case_status = Report.CASE_STATUS.CLOSED

            if previous.manage_by != obj.manage_by and obj.manage_by:
                obj.case_status = Report.CASE_STATUS.OPEN

        super().save_model(request, obj, form, change)


class UserAdmin(admin.ModelAdmin):
    list_display = ('ic_num', 'first_name', 'last_name', 'phone_num', 'role',)
    list_filter = ('role',)
    search_fields = ('ic_num',)


class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'ic_num', 'is_approved',)
    readonly_fields = ('first_name', 'last_name', 'ic_num', 'phone_num', 'email', 'password', 'date_requested',)
    actions = ['approve_requests']

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def approve_requests(self, request, queryset):
        for req in queryset.filter(is_approved=False):
            user = User.objects.create(
                first_name=req.first_name,
                last_name=req.last_name,
                ic_num=req.ic_num,
                phone_num=req.phone_num,
                email=req.email,
                role='co',
            )
            user.password = req.password
            user.save()
            req.is_approved = True
            req.save()
        self.message_user(request, "Selected registration requests approved and users created.")

    def save_model(self, request, obj, form, change):
        if change:
            # Get previous state from DB
            previous = RegistrationRequest.objects.get(pk=obj.pk)

            # Check if is_approved changed from False → True
            if not previous.is_approved and obj.is_approved:
                if not User.objects.filter(ic_num=obj.ic_num).exists():
                    user = User.objects.create(
                        first_name=obj.first_name,
                        last_name=obj.last_name,
                        ic_num=obj.ic_num,
                        phone_num=obj.phone_num,
                        email=obj.email,
                        role='co',
                        password=obj.password  # Already hashed
                    )
                self.message_user(request, "Selected registration requests approved and users created.")
        super().save_model(request, obj, form, change)


admin.site.register(RegistrationRequest, RegistrationRequestAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Notification)
