# franchise_dashboard/services.py

from django.db.models import Q
from core.models import Team
from matches.models import Match, PointsTable


class FranchiseDashboardService:

    @staticmethod
    def get_dashboard(franchise_id):

        # ----------------------------------
        # TEAMS
        # ----------------------------------
        teams = Team.objects.filter(franchise_id=franchise_id)
        team_ids = set(teams.values_list('id', flat=True))

        # ----------------------------------
        # MATCHES (OPTIMIZED)
        # ----------------------------------
        matches = Match.objects.select_related(
            'team1', 'team2', 'venue'
        ).filter(
            Q(team1__in=teams) | Q(team2__in=teams)
        )

        completed_matches = matches.filter(status='completed')

        # ----------------------------------
        # TEAM PERFORMANCE
        # ----------------------------------
        matches_played = completed_matches.count()

        wins = 0

        for m in completed_matches:
            if m.result == 'team1' and m.team1_id in team_ids:
                wins += 1
            elif m.result == 'team2' and m.team2_id in team_ids:
                wins += 1

        losses = matches_played - wins
        win_rate = (wins / matches_played * 100) if matches_played else 0

        # ----------------------------------
        # RUN RATE + ECONOMY
        # ----------------------------------
        total_runs = total_balls = 0
        runs_conceded = balls_bowled = 0

        for m in completed_matches:

            if m.team1_id in team_ids:
                total_runs += m.team1_runs
                total_balls += m.team1_balls
                runs_conceded += m.team2_runs
                balls_bowled += m.team2_balls

            if m.team2_id in team_ids:
                total_runs += m.team2_runs
                total_balls += m.team2_balls
                runs_conceded += m.team1_runs
                balls_bowled += m.team1_balls

        overs = total_balls / 6 if total_balls else 0
        avg_run_rate = round(total_runs / overs, 2) if overs else 0

        overs_bowled = balls_bowled / 6 if balls_bowled else 0
        avg_economy = round(runs_conceded / overs_bowled, 2) if overs_bowled else 0

        # ----------------------------------
        # UPCOMING MATCHES (WITH VENUE)
        # ----------------------------------
        upcoming_matches = matches.filter(
            status='upcoming'
        ).order_by('match_date')[:5]

        upcoming_data = [
            {
                "match": f"{m.team1.team_name} vs {m.team2.team_name}",
                "date": m.match_date,
                "venue": m.venue.ground_name if m.venue else None,
                "city": m.venue.city if m.venue else None
            }
            for m in upcoming_matches
        ]

        # ----------------------------------
        # RECENT MATCHES (MATCH REPORT)
        # ----------------------------------
        recent_matches = completed_matches.order_by('-match_date')[:5]

        recent_data = []

        for m in recent_matches:

            if m.result == 'draw':
                result_text = "Match Draw"

            elif m.result == 'team1':
                margin = abs(m.team1_runs - m.team2_runs)
                if m.team1_id in team_ids:
                    result_text = f"{m.team1.team_name} won by {margin} runs"
                else:
                    result_text = f"Lost"

            elif m.result == 'team2':
                margin = abs(m.team2_runs - m.team1_runs)
                if m.team2_id in team_ids:
                    result_text = f"{m.team2.team_name} won by {margin} runs"
                else:
                    result_text = "Lost"

            recent_data.append({
                "match": f"{m.team1.team_name} vs {m.team2.team_name}",
                "date": m.match_date,
                "venue": m.venue.ground_name if m.venue else None,
                "result": result_text
            })

        # ----------------------------------
        # POINTS TABLE
        # ----------------------------------
        points = PointsTable.objects.select_related('team').filter(
            team__in=teams
        ).order_by('-points')

        points_data = [
            {
                "team": p.team.team_name,
                "played": p.matches_played,
                "wins": p.wins,
                "losses": p.losses,   # ✅ fixed
                "points": p.points,
                "nrr": round(p.net_run_rate, 2)
            }
            for p in points
        ]

        return {
            "team_performance": {
                "matches_played": matches_played,
                "wins": wins,
                "losses": losses,
                "win_rate": round(win_rate, 2),
                "total_runs": total_runs,
                "avg_run_rate": avg_run_rate,
                "avg_economy": avg_economy
            },
            "upcoming_matches": upcoming_data,
            "recent_matches": recent_data,
            "points_table": points_data
        }