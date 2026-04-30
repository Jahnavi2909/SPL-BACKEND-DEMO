from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from accounts.permissions import IsFranchise, IsAdmin, IsAdminOrFranchise
from .models import Team, Player
from .serializers import TeamSerializer, PlayerSerializer,TeamDetailWithPlayersSerializer,TeamPlayerFullSerializer,teamSerializer
from .pagination import TeamPagination, PlayerPagination
from django.db.models import Count

# ===================== TEAM APIs ===================== #s

class CreateTeamView(APIView):
    permission_classes = [IsAdminOrFranchise]

    def post(self, request):
        serializer = TeamSerializer(data=request.data)

        if serializer.is_valid():
            if request.user.role == "ADMIN":
                franchise_id = request.data.get("franchise")
                serializer.save(franchise_id=franchise_id, is_approved=True)
            else:
                serializer.save(franchise=request.user.franchise)

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApproveTeamView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        team = Team.objects.get(id=pk)
        team.is_approved = True
        team.save()
        return Response({"message": "Team Approved"})


class TeamListView(ListAPIView):
    queryset = Team.objects.all().annotate(player_count=Count('players'))
    serializer_class = TeamSerializer
    pagination_class = TeamPagination

    def get_queryset(self):
        queryset = Team.objects.annotate(
            player_count=Count('players')
        )


        status = self.request.query_params.get('status') 
        franchise = self.request.query_params.get('franchise')
        team = self.request.query_params.get('team')
        

        if franchise:
            queryset = queryset.filter(franchise__name__icontains=franchise)

        if team:
            queryset = queryset.filter(team_name__icontains=team)

        return queryset

    # pagination control
    def paginate_queryset(self, queryset):
        if self.request.query_params.get('all', '').lower().strip() == 'true':
            return None
        return super().paginate_queryset(queryset)


class TeamDetailView(RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamUpdateView(UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, IsAdminOrFranchise]

    def perform_update(self, serializer):
        team = self.get_object()

        if self.request.user.role == "ADMIN":
            serializer.save()
        elif team.franchise == self.request.user.franchise:
            serializer.save()
        else:
            raise PermissionDenied("Not your team")


class TeamDeleteView(DestroyAPIView):
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrFranchise]

    def perform_destroy(self, instance):
        if self.request.user.role == "ADMIN":
            instance.delete()
        elif instance.franchise == self.request.user.franchise:
            instance.delete()
        else:
            raise PermissionDenied("Not your team")


# ===================== PLAYER APIs ===================== #

# class CreatePlayerView(APIView):
#     permission_classes = [IsAdminOrFranchise]

#     def post(self, request):
#         team_id = request.data.get("team")
#         team = Team.objects.filter(id=team_id).first()

#         if not team:
#             return Response({"error": "Team not found"}, status=404)

#         if request.user.role == "ADMIN":
#             serializer = PlayerSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(team=team)
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         else:
#             if team.franchise != request.user.franchise:
#                 return Response({"error": "Not your team"}, status=403)

#             if not team.is_approved:
#                 return Response({"error": "Team not approved"}, status=400)

#             serializer = PlayerSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(team=team)
#                 return Response(serializer.data)

#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CreatePlayerView(APIView):
    permission_classes = [IsAdminOrFranchise]
 
    def post(self, request):
        team_id = request.data.get("team")
        team = Team.objects.filter(id=team_id).first()
 
        if not team:
            return Response({"error": "Team not found"}, status=404)
 
        if request.user.role == "ADMIN":
            serializer = PlayerSerializer(data=request.data)
 
            if serializer.is_valid():
                player = serializer.save(team=team)
                return Response(
                    PlayerSerializer(player).data,
                    status=status.HTTP_201_CREATED
                )
 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        else:
            if team.franchise != request.user.franchise:
                return Response({"error": "Not your team"}, status=403)
 
            if not team.is_approved:
                return Response({"error": "Team not approved"}, status=400)
 
            serializer = PlayerSerializer(data=request.data)
 
            if serializer.is_valid():
                player = serializer.save(team=team)
                return Response(
                    PlayerSerializer(player).data,
                    status=status.HTTP_201_CREATED
                )
 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

















class PlayerListView(ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    pagination_class = PlayerPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        player = self.request.query_params.get('player')
        team = self.request.query_params.get('team')
        franchise = self.request.query_params.get('franchise')

        if player:
            queryset = queryset.filter(player_name__icontains=player)

        if team:
            queryset = queryset.filter(team__team_name__icontains=team)

        if franchise:
            queryset = queryset.filter(team__franchise__name__icontains=franchise)

        return queryset

    # ✅ pagination control
    def paginate_queryset(self, queryset):
        if self.request.query_params.get('all', '').lower().strip() == 'true':
            return None
        return super().paginate_queryset(queryset)


class PlayerDetailView(RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerUpdateView(UpdateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated, IsAdminOrFranchise]

    def perform_update(self, serializer):
        player = self.get_object()

        if self.request.user.role == "ADMIN":
            serializer.save()
        elif player.team.franchise == self.request.user.franchise:
            serializer.save()
        else:
            raise PermissionDenied("Not your player")


class PlayerDeleteView(DestroyAPIView):
    queryset = Player.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrFranchise]

    def perform_destroy(self, instance):
        if self.request.user.role == "ADMIN":
            instance.delete()
        elif instance.team.franchise == self.request.user.franchise:
            instance.delete()
        else:
            raise PermissionDenied("Not your player")


# ===================== EXTRA ===================== #

class TeamPlayersView(ListAPIView):
    serializer_class = PlayerSerializer
    pagination_class = PlayerPagination

    def get_queryset(self):
        team_id = self.kwargs['pk']
        return Player.objects.filter(team_id=team_id)

    # pagination control
    def paginate_queryset(self, queryset):
        if self.request.query_params.get('all', '').lower().strip() == 'true':
            return None
        return super().paginate_queryset(queryset)








class FranchiseTeamDetailAPIView(APIView):

    def get(self, request, franchise_id, team_id):
        try:
            team = Team.objects.get(id=team_id, franchise_id=franchise_id)
        except Team.DoesNotExist:
            return Response(
                {"error": "Team not found for this franchise"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeamDetailWithPlayersSerializer(team)
        return Response(serializer.data)




class FranchiseTeamPlayerFullAPIView(APIView):

    def get(self, request, franchise_id, team_id, player_id):
        try:
            team = Team.objects.prefetch_related('players').get(
                id=team_id,
                franchise_id=franchise_id
            )
        except Team.DoesNotExist:
            return Response(
                {"error": "Team not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not team.players.filter(id=player_id).exists():
            return Response(
                {"error": "Player not in this team"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeamPlayerFullSerializer(
            team,
            context={'player_id': player_id}
        )

        return Response(serializer.data)






from rest_framework.generics import RetrieveAPIView
from .models import Player
from .serializers import PlayerFullDetailSerializer


class PlayerFullDetailAPIView(RetrieveAPIView):
    queryset = Player.objects.select_related("team", "playerstats").prefetch_related("team__players")
    serializer_class = PlayerFullDetailSerializer


class teamListView(ListAPIView):
    queryset = Team.objects.all().annotate(player_count=Count('players'))
    serializer_class = teamSerializer
    pagination_class = TeamPagination
 
    def get_queryset(self):
        queryset = super().get_queryset()
 
        franchise = self.request.query_params.get('franchise')
        team = self.request.query_params.get('team')
 
        if franchise:
            queryset = queryset.filter(franchise__name__icontains=franchise)
 
        if team:
            queryset = queryset.filter(team_name__icontains=team)
 
        return queryset
 
    # pagination control
    def paginate_queryset(self, queryset):
        if self.request.query_params.get('all', '').lower().strip() == 'true':
            return None
        return super().paginate_queryset(queryset)






