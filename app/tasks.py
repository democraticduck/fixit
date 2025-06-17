from celery import shared_task
from django.utils import timezone
from .models import Report, Notification

@shared_task
def notify_overdue_reports():
    now = timezone.now()
    reports = Report.objects.filter(case_status__in=['op', 'ip'])

    for report in reports:
        days_since_update = (now - report.updated_at).days

        # Notify only if it's a multiple of 7 days and not zero
        #if days_since_update >= 7 and days_since_update % 7 == 0:
        if days_since_update >= 7 and days_since_update % 7 == 0:
            # Check if a notification has already been sent for this day count
            existing = Notification.objects.filter(report=report, sent_at__date=now.date())
            if not existing.exists():
                Notification.objects.create(
                    title=f"Reminder: {report.title}",
                    description=f"This report has not been updated for {days_since_update} days. Please review and take necessary action.",
                    sent_at=now,
                    report=report
                )
