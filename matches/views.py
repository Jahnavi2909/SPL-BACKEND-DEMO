# views.py

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
from django.db import transaction
 
from .models import Match, PlayingXI, PointsTable, PlayerStats
from .serializers import (
    MatchListSerializer,
    PlayingXISerializer,
    PointsTableSerializer,
    PlayerStatsSerializer,
    matchgetserializers
)
from .permissions import (
    IsAuthenticatedOrReadOnlyCustom,
    IsAdminUserCustom
)
 
from .services import (
    update_points_table,
    calculate_derived_fields,
    calculate_player_points,
    recalculate_player_stats
)
 
 
# GET /api/matches/
class MatchListView(ListAPIView):
    queryset = Match.objects.all().order_by('-id')
    serializer_class = MatchListSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCustom]
 
 
# GET /api/matches/36/
class MatchDetailView(RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class =matchgetserializers
    permission_classes = [IsAuthenticatedOrReadOnlyCustom]
 
 
# GET + PUT + PATCH
# /api/matches/36/edit/
class MatchUpdateView(RetrieveUpdateAPIView):
    queryset = Match.objects.all()
    serializer_class = matchgetserializers
    permission_classes = [IsAdminUserCustom]
 
 
class PlayingXIViewSet(viewsets.ModelViewSet):
    queryset = PlayingXI.objects.all()
    serializer_class = PlayingXISerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCustom]
 
    def perform_create(self, serializer):
        players = serializer.validated_data.get('players')
        captain = serializer.validated_data.get('captain')
        team = serializer.validated_data.get('team')
 
        if len(players) != 11:
            raise ValidationError("Exactly 11 players required")
 
        if captain not in players:
            raise ValidationError("Captain must be in playing XI")
 
        for player in players:
            if player.team != team:
                raise ValidationError("Players must belong to same team")
 
        serializer.save()
 
 
class PointsTableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PointsTable.objects.all().order_by('-points', '-net_run_rate')
    serializer_class = PointsTableSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyCustom]
 
 
class PlayerStatsViewSet(viewsets.ModelViewSet):
    queryset = PlayerStats.objects.all().order_by('-total_runs')
    serializer_class = PlayerStatsSerializer
 
 
class TopPerformerCardAPIView(APIView):
    def get(self, request):
        top_batter = PlayerStats.objects.order_by('-total_runs').first()
        top_bowler = PlayerStats.objects.order_by('-wickets').first()
 
        batter_data = None
        bowler_data = None
 
        if top_batter:
            batter_data = {
                "player_id": top_batter.player.id,
                "player_name": top_batter.player.player_name,
                "team_name": top_batter.player.team.team_name,
                "matches": top_batter.matches,
                "score": top_batter.total_runs,
                "average": round(top_batter.strike_rate, 1)
            }
 
        if top_bowler:
            bowler_data = {
                "player_id": top_bowler.player.id,
                "player_name": top_bowler.player.player_name,
                "team_name": top_bowler.player.team.team_name,
                "wickets": top_bowler.wickets,
                "matches": top_bowler.matches,
                "economy": round(top_bowler.economy, 1)
            }
 
        return Response({
            "top_batter": batter_data,
            "top_bowler": bowler_data
        })