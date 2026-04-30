from django.db import models
from accounts.models import Franchise

from django.db import models
from django.db.models.functions import Lower

from django.db import models
from django.db.models.functions import Lower

class Team(models.Model):
    franchise = models.ForeignKey('accounts.Franchise', on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=5, default=False)
    home_city = models.CharField(max_length=20, default=False)
    head_coach = models.CharField(max_length=30, default=False)
    home_ground = models.CharField(max_length=40, default=False)
    captain = models.ForeignKey(
        'Player',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='captain_of'
    )
    primary_color = models.CharField(max_length=50, default=False)
    logo = models.ImageField(upload_to='teams_logo/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('team_name'),
                name='unique_team_name_case_insensitive'
            )
        ]

    def __str__(self):
        return self.team_name

class Player(models.Model):
    ROLE_CHOICES = [
        ('RIGHT_HAND_BATTER', 'right_hand_batter'),
        ('LEFT_HAND_BATTER', 'left_hand_batter')
    ]
    BOWLING_CHOICES = [
        ('RIGHT_ARM_FAST', 'right_arm_fast'),
        ('LEFT_ARM_FAST', 'left_arm_fast'),
        ('RIGHT_ARM_SPIN', 'right_arm_spin'),
        ('LEFT_ARM_SPIN', 'left_arm_spin'),
    ]
    ROLE_CHOICESS=[
        ('Bowling','bowling'),
        ('Batting','batting'),
        ('AllRounder','allrounder')
    ]
    team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='players')
    player_name = models.CharField(max_length=100)
    age = models.IntegerField(default=25)
    date_of_birth = models.DateField(null=True,blank=True)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    role=models.CharField(max_length=20,choices=ROLE_CHOICESS,default='Batting')
    Batting_Style = models.CharField(max_length=20,choices=ROLE_CHOICES,default='RIGHT_HAND_BATTER')
    Bowling_style = models.CharField(max_length=20,choices=BOWLING_CHOICES,default='RIGHT_ARM_FAST')
    photo = models.ImageField(upload_to='player_photo/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.player_name
    


