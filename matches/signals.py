from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Team,Player
from .models import Match, PointsTable, PlayerStats
from .services import update_points_table







@receiver(post_save, sender=Player)
def create_player_stats(sender, instance, created, **kwargs):
    if created:
        PlayerStats.objects.create(player=instance)








@receiver(post_save, sender=Team)
def handle_team_post_save(sender, instance, created, **kwargs):

    # Only proceed if team is approved
    if not instance.is_approved:
        return

    # 1. CREATE POINTS TABLE ENTRY (NEW LOGIC)
    PointsTable.objects.get_or_create(team=instance)

    #2. EXISTING FIXTURE LOGIC (your code)
    teams = Team.objects.filter(is_approved=True).exclude(id=instance.id)

    for team in teams:
        exists = Match.objects.filter(
            team1=instance, team2=team
        ).exists() or Match.objects.filter(
            team1=team, team2=instance
        ).exists()

        if not exists:
            Match.objects.create(
                team1=instance,
                team2=team,
                status='pending'
            )






@receiver(post_save, sender=Match)
def update_points_on_match_save(sender, instance, created, **kwargs):

    print("Signal triggered for match:", instance.id)
    print("STATUS:", instance.status)
    print("LOCKED:", instance.is_locked)
    print("POINTS UPDATED:", instance.points_updated)

    if created:
        print("Skipped: created")
        return

    if instance.status == 'completed' and instance.is_locked:

        if instance.points_updated:
            print("Skipped: already updated")
            return

        print("Updating points table...")
        update_points_table(instance)
    else:
        print("Condition failed")