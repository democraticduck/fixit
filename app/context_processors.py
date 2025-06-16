from django.db.models import Q
from .models import Notification

def notification_context(request):
    context = {}

    if request.user.is_authenticated:
        user = request.user

        status_notifications = Notification.objects.filter(
            report__user_id=user,
            description__startswith="The"
        )

        reminder_notifications = Notification.objects.filter(
            report__manage_by=user,
        ).filter(
            Q(description__startswith="You") | Q(description__startswith="This")
        )

        context['notifications'] = (
            status_notifications.union(reminder_notifications)
            .order_by('-sent_at')
        )

    return context
