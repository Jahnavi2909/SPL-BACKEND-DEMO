from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Team, PointsTable

@receiver(post_save, sender=Team)
def create_points_table(sender, instance, created, **kwargs):
    if instance.is_approved:
        PointsTable.objects.get_or_create(team=instance)