from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db import models
from .models import Report, Notification

@shared_task
def check_overdue_reports_and_notify():
    now = timezone.now()
    reports = Report.objects.filter(status__in=['op', 'ip'])

    for report in reports:
        days_since_update = (now - report.updated_at).days

        # Notify only if it's a multiple of 7 days and not zero
        if days_since_update >= 7 and days_since_update % 7 == 0:
            # Check if a notification has already been sent for this day count
            existing = Notification.objects.filter(report_id=report, sent_at__date=now.date())
            if not existing.exists():
                Notification.objects.create(
                    description=f"Reminder: This report has not been updated for {days_since_update} days. Please review and take necessary action.",
                    sent_at=now,
                    report_id=report
                )

@shared_task
def check_status_updates_and_notify():
    now = timezone.now()
    threshold_time = now - timedelta(days=1)

    # Filter reports updated in the last few seconds but not newly created
    recent_reports = Report.objects.filter(
        updated_at__gte=threshold_time
    ).exclude(
        updated_at=models.F('created_at')  # Exclude new reports
    )

    for report in recent_reports:
        already_notified = Notification.objects.filter(
            report_id=report,
            sent_at__gte=threshold_time,
            description__startswith="The status"
        )
        if not already_notified.exists():
            Notification.objects.create(
                description="The status of your report has been updated. Please check for details.",
                sent_at=now,
                report_id=report
            )
