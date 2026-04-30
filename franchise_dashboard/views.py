from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Max, Q

from core.models import Team, Player
from matches.models import Match, PlayerStats


class FranchiseDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'franchise'):
            return Response({"error": "No franchise assigned"}, status=400)

        franchise = user.franchise

        # =========================================
        # 🔹 TEAMS & PLAYERS
        # =========================================
        teams = Team.objects.filter(franchise=franchise)
        players = Player.objects.filter(team__in=teams)

        total_players = players.count()
        active_teams = teams.filter(is_approved=True).count()

        # =========================================
        # 🔹 MATCHES
        # =========================================
        matches = Match.objects.filter(
            Q(team1__in=teams) | Q(team2__in=teams),
            status='completed'
        )

        matches_played = matches.count()

        wins = matches.filter(
            Q(team1__in=teams, result='team1') |
            Q(team2__in=teams, result='team2')
        ).count()

        win_rate = (wins / matches_played * 100) if matches_played else 0

        # =========================================
        # 🔹 RECENT MATCHES
        # =========================================
        recent_matches_qs = matches.order_by('-match_date')[:5]

        recent_matches = []
        for m in recent_matches_qs:
            if m.team1 in teams:
                opponent = m.team2.team_name
                result = "Win" if m.result == 'team1' else "Loss"
            else:
                opponent = m.team1.team_name
                result = "Win" if m.result == 'team2' else "Loss"

            recent_matches.append({
                "opponent": opponent,
                "result": result
            })

        # =========================================
        # 🔹 UPCOMING MATCH (NEXT ONE)
        # =========================================
        upcoming = Match.objects.filter(
            Q(team1__in=teams) | Q(team2__in=teams),
            status='upcoming'
        ).order_by('match_date').first()

        upcoming_data = None
        if upcoming:
            upcoming_data = {
                "team1": upcoming.team1.team_name,
                "team2": upcoming.team2.team_name,
                "date": upcoming.match_date,
                "venue": upcoming.venue.name if upcoming.venue else None,
                "city": upcoming.venue.city if upcoming.venue else None
            }

        # =========================================
        # 🔹 PLAYER STATS
        # =========================================
        stats = PlayerStats.objects.filter(player__in=players)

        highest_score = stats.aggregate(max=Max('total_runs'))['max'] or 0
        best_bowling = stats.aggregate(max=Max('wickets'))['max'] or 0

        # biggest win (runs difference)
        biggest_win = 0
        for m in matches:
            diff = abs(m.team1_runs - m.team2_runs)
            if diff > biggest_win:
                biggest_win = diff

        # =========================================
        # 🔹 TOP PERFORMERS (TABLE)
        # =========================================
        top_players = stats.order_by('-total_runs')[:5]

        top_performers = []
        for p in top_players:
            top_performers.append({
                "player": p.player.player_name,
                "role": p.role,
                "runs": p.total_runs,
                "wickets": p.wickets,
                "strike_rate": round(p.strike_rate, 1)
            })

        # =========================================
        # 🔹 FINAL RESPONSE
        # =========================================
        return Response({
            "cards": {
                "total_players": total_players,
                "active_teams": active_teams,
                "matches_played": matches_played,
                "win_rate": round(win_rate, 1)
            },

            "recent_matches": recent_matches,

            "upcoming_match": upcoming_data,

            "season_highlights": {
                "highest_score": highest_score,
                "best_bowling": best_bowling,
                "biggest_win": biggest_win
            },

            "top_performers": top_performers
        })





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Max, Q

from core.models import Team, Player
from matches.models import Match, PlayerStats


class FranchiseTeamPerformanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'franchise'):
            return Response({"error": "No franchise assigned"}, status=400)

        franchise = user.franchise

        # =========================================
        # 🔹 TEAMS
        # =========================================
        teams = Team.objects.filter(franchise=franchise)

        # =========================================
        # 🔹 MATCHES
        # =========================================
        matches = Match.objects.filter(
            Q(team1__in=teams) | Q(team2__in=teams),
            status='completed'
        )

        total_matches = matches.count()

        wins = matches.filter(
            Q(team1__in=teams, result='team1') |
            Q(team2__in=teams, result='team2')
        ).count()

        losses = matches.filter(
            Q(team1__in=teams, result='team2') |
            Q(team2__in=teams, result='team1')
        ).count()

        win_percentage = (wins / total_matches * 100) if total_matches else 0

        # =========================================
        # 🔹 PLAYER STATS (ALL TEAMS)
        # =========================================
        players = Player.objects.filter(team__in=teams)
        stats = PlayerStats.objects.filter(player__in=players)

        total_runs = stats.aggregate(total=Sum('total_runs'))['total'] or 0
        total_wickets = stats.aggregate(total=Sum('wickets'))['total'] or 0
        highest_score = stats.aggregate(max=Max('total_runs'))['max'] or 0

        # =========================================
        # 🔹 TOP PERFORMERS
        # =========================================
        top_batsmen = stats.order_by('-total_runs')[:2]
        top_bowler = stats.order_by('-wickets').first()

        top_performers = []

        for b in top_batsmen:
            top_performers.append({
                "player_name": b.player.player_name,
                "runs": b.total_runs
            })

        if top_bowler:
            top_performers.append({
                "player_name": top_bowler.player.player_name,
                "wickets": top_bowler.wickets
            })

        # =========================================
        # 🔹 RECENT MATCHES
        # =========================================
        recent_matches_qs = matches.order_by('-match_date')[:5]

        recent_matches = []

        for m in recent_matches_qs:
            if m.team1 in teams:
                opponent = m.team2.team_name
                result = "Win" if m.result == 'team1' else "Loss"
            else:
                opponent = m.team1.team_name
                result = "Win" if m.result == 'team2' else "Loss"

            recent_matches.append({
                "opponent": opponent,
                "result": result
            })

        # =========================================
        # 🔹 FINAL RESPONSE
        # =========================================
        return Response({
            "matches": total_matches,
            "wins": wins,
            "losses": losses,
            "win_percentage": round(win_percentage, 1),

            "performance": {
                "total_runs": total_runs,
                "total_wickets": total_wickets,
                "highest_score": highest_score
            },

            "top_performers": top_performers,

            "recent_matches": recent_matches
        })





