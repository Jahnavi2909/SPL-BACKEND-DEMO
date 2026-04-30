from rest_framework import serializers
from django.conf import settings

from .models import Team, Player
from matches.models import PlayerStats






class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.team_name', read_only=True)
    franchise_name = serializers.CharField(source='team.franchise.name', read_only=True)
    photo = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Player
        fields = [
            'id',
            'player_name',
            'age',
            'date_of_birth',
            'mobile',
            'email',
            'Batting_Style',
            'Bowling_style',
            'role',
            'photo',
            'created_at',
            'team',
            'team_name',
            'franchise_name'
        ]

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.url
        return None
class TeamSerializer(serializers.ModelSerializer):
    franchise_name = serializers.CharField(source='franchise.name', read_only=True)
    logo = serializers.ImageField(required=False, allow_null=True)
    player_count = serializers.IntegerField(read_only=True)
    players=PlayerSerializer(many=True,read_only=True)
    class Meta:
        model = Team
        fields = [
            'id',
            'team_name',
            'short_name',
            'home_city',
            'head_coach',
            'home_ground',
            'primary_color',
            'logo',
            'captain',
            'is_approved',
            'created_at',
            'franchise',
            'franchise_name',
            'player_count',
            'players'
        ]
        read_only_fields = ['is_approved', 'franchise']
        def validate_team_name(self, value):
            qs = Team.objects.filter(team_name__iexact=value)

        # exclude current instance (important for update)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)

            if qs.exists():
                raise serializers.ValidationError("Team name already exists.")

            return value

    def get_logo(self, obj):
        if obj.logo:
            return obj.logo.url  
        return None
    def get_player_count(self, obj):
        return obj.player.count()



class PlayerMiniSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.team_name', read_only=True)
    franchise_name = serializers.CharField(source='team.franchise.name', read_only=True)
   
    
    class Meta:
        model = Player
        fields = [
            'id',
            'player_name',
            'age',
            'date_of_birth',
            'mobile',
            'email',
            'Batting_Style',
            'Bowling_style',
            'photo',
            'team',
            'team_name',
            'franchise_name',
            
        ]


class TeamDetailWithPlayersSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField()
    player_count = serializers.SerializerMethodField()  # ✅ add here

    class Meta:
        model = Team
        fields = [
            'id',
            'team_name',
            'short_name',
            'home_city',
            'head_coach',
            'home_ground',
            'primary_color',
            'logo',
            'player_count',   # ✅ include here
            'players'
        ]

    def get_players(self, obj):
        return PlayerMiniSerializer(obj.players.all(), many=True).data

    def get_player_count(self, obj):
        return obj.players.count()






class TeamPlayerFullSerializer(serializers.ModelSerializer):
    player = serializers.SerializerMethodField()
    squad = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'player',   # ✅ first
            'id',
            'team_name',
            'short_name',
            'home_city',
            'head_coach',
            'home_ground',
            'primary_color',
            'logo',
            'squad'     # ✅ full squad
        ]

    def get_player(self, obj):
        player_id = self.context.get('player_id')
        player = obj.players.filter(id=player_id).first()
        if not player:
            return None
        return PlayerMiniSerializer(player).data

    def get_squad(self, obj):
        players = obj.players.all()
        return PlayerMiniSerializer(players, many=True).data








# ✅ Squad minimal
class SquadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            "id",
            "player_name",
            "role",
            "Batting_Style",
            "Bowling_style",
            "photo"
        ]


# ✅ MAIN serializer
class PlayerFullDetailSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    stats=serializers.SerializerMethodField() 

    class Meta:
        model = Player
        fields = [
            "id",
            "player_name",
            "age",
            "created_at",
            "date_of_birth",
            "role",
            "Batting_Style",
            "Bowling_style",
            "photo",
            "stats",
            "team"
        ]

    def get_team(self, obj):
        team = obj.team

        return {
            "id": team.id,
            "team_name": team.team_name,
            "short_name": team.short_name,
            "home_city": team.home_city,
            "head_coach": team.head_coach,
            "home_ground": team.home_ground,
            "primary_color": team.primary_color,
            "logo": team.logo.url if team.logo else None,

            # ✅ FULL SQUAD
            "squad": SquadSerializer(team.players.all(), many=True).data
        }

    def get_stats(self, obj):
        stats = PlayerStats.objects.filter(player=obj).first()

        if not stats:
            return None

        return {
            "matches": stats.matches,
            "total_runs": stats.total_runs,
            "balls_faced": stats.balls_faced,
            "wickets": stats.wickets,
            "overs_bowled": stats.overs_bowled,
            "runs_conceded": stats.runs_conceded,
            "strike_rate": stats.strike_rate,
            "economy": stats.economy
        }


class teamSerializer(serializers.ModelSerializer):
    franchise_name = serializers.CharField(source='franchise.name', read_only=True)
    logo = serializers.ImageField(required=False, allow_null=True)
    player_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Team
        fields = [
            'id',
            'team_name',
            'short_name',
            'home_city',
            'head_coach',
            'home_ground',
            'primary_color',
            'logo',
            'captain',
            'is_approved',
            'created_at',
            'franchise',
            'franchise_name',
            'player_count',
        ]
        # read_only_fields = ['is_approved', 'franchise']
        # def validate_team_name(self, value):
        #     qs = Team.objects.filter(team_name__iexact=value)
 
        # # exclude current instance (important for update)
        #     if self.instance:
        #         qs = qs.exclude(id=self.instance.id)
 
        #     if qs.exists():
        #         raise serializers.ValidationError("Team name already exists.")
 
        #     return value
 
    def get_logo(self, obj):
        if obj.logo:
            return obj.logo.url  
        return None
    def get_player_count(self, obj):
        return obj.player.count()