from .models import Notification

def notification_context(request):
    context = {}

    if request.user.is_authenticated:
        user = request.user

        status_notifications = Notification.objects.filter(
            report_id__user_id=user,
            description__startswith="The status"
        )

        reminder_notifications = Notification.objects.filter(
            report_id__manage_by=user,
            description__startswith="Reminder"
        )

        context['notifications'] = (
            status_notifications.union(reminder_notifications)
            .order_by('-sent_at')
        )

    return context
