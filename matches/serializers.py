# serializers.py
 
from rest_framework import serializers
from .models import Match, PlayingXI, PointsTable, PlayerStats
from veneus.models import Venue
from core.models import Team
 
 
 
class matchgetserializers(serializers.ModelSerializer):
    class Meta:
        model=Match
        fields='__all__'
 
class TeamMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'team_name']
 
 
class VenueMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'ground_name']
 
class MatchListSerializer(serializers.ModelSerializer):
    team1 = TeamMiniSerializer(read_only=True)
    team2 = TeamMiniSerializer(read_only=True)
    venue = VenueMiniSerializer(read_only=True)
 
    class Meta:
        model = Match
        fields = [
            'id',
            'team1',
            'team2',
            'match_date',
            'venue',
            'result'
        ]
 
 
class PlayingXISerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayingXI
        fields = '__all__'
 
 
class PointsTableSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.team_name', read_only=True)
 
    class Meta:
        model = PointsTable
        fields = [
            'team_name',
            'matches_played',
            'wins',
            'losses',
            'net_run_rate',
            'points'
        ]
 
 
class PlayerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStats
        fields = '__all__'
 





