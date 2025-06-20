# app/observers.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Report, Notification

# Store the old state of reports before saving
@receiver(pre_save, sender=Report)
def store_old_report_state(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_instance = Report.objects.get(pk=instance.pk)
        except Report.DoesNotExist:
            instance._old_instance = None

@receiver(post_save, sender=Report)
def report_observer(sender, instance, created, **kwargs):
    now = timezone.now()

    if created:
        return  # No notification needed on report creation

    old = getattr(instance, '_old_instance', None)
    if not old:
        return

    # 1. Admin approves/rejects a report
    if old.approve_status != instance.approve_status:
        if instance.approve_status == 'ap':
            Notification.objects.create(
                title=f"Approved: {instance.title}",
                description="Your report has been approved by the admin.",
                sent_at=now,
                report=instance,
            )
        elif instance.approve_status == 'rj':
            Notification.objects.create(
                title=f"Rejected: {instance.title}",
                description="Your report has been rejected by the admin.",
                sent_at=now,
                report=instance,
            )

    # 2. Coordinator is assigned to the report
    if old.manage_by != instance.manage_by and instance.manage_by is not None:
        Notification.objects.create(
            title=f"New: {instance.title}",
            description=f"You have been assigned to manage the case: \"{instance.title}\".",
            sent_at=now,
            report=instance,
        )

    # 3. Coordinator updates status or progress
    if (
        old.manage_by == instance.manage_by and instance.manage_by is not None and
        (old.case_status != instance.case_status or old.progress_detail != instance.progress_detail)
    ):
        Notification.objects.create(
            title=f"Update: {instance.title}",
            description="The status of your case has been updated. Please check the details.",
            sent_at=now,
            report=instance,
        )
