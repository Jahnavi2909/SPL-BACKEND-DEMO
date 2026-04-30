from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q

from core.models import Team,Player
from veneus.models import Venue




from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q

from core.models import Team,Player
from veneus.models import Venue


class Match(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('live', 'Live'),
    )

    RESULT_CHOICES = (
        ('team1', 'Team1'),
        ('team2', 'Team2'),
        ('draw', 'Draw'),
        ('pending', 'Pending'),
    )

    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches')

    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
    match_date = models.DateTimeField(null=True, blank=True)
    Umpire1=models.CharField(max_length=30,null=True,blank=True)
    Umpire2=models.CharField(max_length=30,null=True,blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='pending')

    # ✅ SCORE (IMPORTANT)
    team1_runs = models.IntegerField(default=0)
    team1_balls = models.IntegerField(default=0)

    team2_runs = models.IntegerField(default=0)
    team2_balls = models.IntegerField(default=0)

    # 🔒 LOCK SYSTEM
    is_locked = models.BooleanField(default=False)
    points_updated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 VALIDATION
    def clean(self):

        # ❌ Same team
        if self.team1 == self.team2:
            raise ValidationError("Both teams cannot be same")

        # ❌ One match per day
        if self.match_date:
            existing = Match.objects.filter(
                Q(team1=self.team1) | Q(team2=self.team1) |
                Q(team1=self.team2) | Q(team2=self.team2),
                match_date__date=self.match_date.date()
            ).exclude(id=self.id)

            if existing.exists():
                raise ValidationError("One team can play only one match per day")

        # 🔒 LOCK CHECK
        if self.pk:
            old = Match.objects.get(pk=self.pk)

    # ❌ block edits only if locked AND not updating points_updated
            if old.is_locked:
        # allow only points_updated update
                if not (
                    self.points_updated != old.points_updated and
                    self.result == old.result and
                    self.team1_runs == old.team1_runs and
                    self.team2_runs == old.team2_runs
                ):
                    raise ValidationError("Match is locked. Cannot edit.")

        # ✅ RESULT VALIDATION (VERY IMPORTANT)
        if self.result != 'pending':

            if self.team1_runs == self.team2_runs and self.result != 'draw':
                raise ValidationError("Match is draw, result must be 'draw'")

            if self.team1_runs > self.team2_runs and self.result != 'team1':
                raise ValidationError("Team1 should be winner")

            if self.team2_runs > self.team1_runs and self.result != 'team2':
                raise ValidationError("Team2 should be winner")

    # 🔥 AUTO STATUS
    def save(self, *args, **kwargs):

        if self.match_date:
            if self.match_date > timezone.now():
                self.status = 'upcoming'
            else:
                self.status = 'completed'
        else:
            self.status = 'pending'

        # 🔥 IMPORTANT: run validation before save
        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team1} vs {self.team2}"

class PlayingXI(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    players = models.ManyToManyField(Player)
    captain = models.CharField(max_length=30)

    class Meta:
        unique_together = ['match', 'team']  # ✅ prevent duplicates

    def clean(self):
        # ✅ team must be part of match
        if self.team not in [self.match.team1, self.match.team2]:
            raise ValidationError("Team must be part of the match")

    def __str__(self):
        return f"{self.team} XI"

class PointsTable(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    matches_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    net_run_rate = models.FloatField(default=0.0)
    points = models.IntegerField(default=0)

    runs_scored = models.IntegerField(default=0)
    balls_faced = models.IntegerField(default=0)

    runs_conceded = models.IntegerField(default=0)
    balls_bowled = models.IntegerField(default=0)

    def __str__(self):
        return self.team.team_name

class MatchPlayingXI(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)

    team1_players = models.ManyToManyField(Player, related_name='team1_players')
    team2_players = models.ManyToManyField(Player, related_name='team2_players')

    team1_captain = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='team1_captain'
    )
    team2_captain = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='team2_captain'
    )

    def clean(self):
        # ⚠️ DO NOT use ManyToMany here
        if not self.match:
            raise ValidationError("Match is required")

    def __str__(self):
        return f"{self.match} Playing XI"




class PlayerStats(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)

    # basic info (auto)
    player_name = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20)

    # editable stats
    matches = models.IntegerField(default=0)
    total_runs = models.IntegerField(default=0)
    balls_faced = models.IntegerField(default=0)

    wickets = models.IntegerField(default=0)
    overs_bowled = models.FloatField(default=0)
    runs_conceded = models.IntegerField(default=0)

    # auto calculated
    strike_rate = models.FloatField(default=0)
    economy = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        # auto fill player info
        self.player_name = self.player.player_name
        self.team_name = self.player.team.team_name
        self.role = self.player.role

        # strike rate
        if self.balls_faced > 0:
            self.strike_rate = (self.total_runs / self.balls_faced) * 100
        else:
            self.strike_rate = 0

        # economy
        if self.overs_bowled > 0:
            self.economy = self.runs_conceded / self.overs_bowled
        else:
            self.economy = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return self.player_name


