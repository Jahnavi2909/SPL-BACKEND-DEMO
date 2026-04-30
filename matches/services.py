from django.db.models import Sum


def update_points_table(match):
    from .models import PointsTable

    if match.points_updated:
        return

   

    t1, _ = PointsTable.objects.get_or_create(team=match.team1)
    t2, _ = PointsTable.objects.get_or_create(team=match.team2)

    # matches played
    t1.matches_played += 1
    t2.matches_played += 1

    #  result logic
    if match.result == 'team1':
        t1.wins += 1
        t2.losses += 1
        t1.points += 2

    elif match.result == 'team2':
        t2.wins += 1
        t1.losses += 1
        t2.points += 2

    elif match.result == 'draw':
        t1.points += 1
        t2.points += 1

    # RUNS + BALLS
    t1.runs_scored += match.team1_runs
    t1.balls_faced += match.team1_balls
    t1.runs_conceded += match.team2_runs
    t1.balls_bowled += match.team2_balls

    t2.runs_scored += match.team2_runs
    t2.balls_faced += match.team2_balls
    t2.runs_conceded += match.team1_runs
    t2.balls_bowled += match.team1_balls

    # NRR calculation
    def calc(team):
        if team.balls_faced > 0 and team.balls_bowled > 0:
            overs_faced = team.balls_faced / 6
            overs_bowled = team.balls_bowled / 6

            return round(
                (team.runs_scored / overs_faced) -
                (team.runs_conceded / overs_bowled),
                3  #  keep 3 decimals like IPL
            )
        return 0

    t1.net_run_rate = calc(t1)
    t2.net_run_rate = calc(t2)

    t1.save()
    t2.save()

    # mark match updated (VERY IMPORTANT)
    from .models import Match
    Match.objects.filter(id=match.id).update(points_updated=True)







def calculate_derived_fields(obj):
    # Strike Rate
    if obj.balls > 0:
        obj.strike_rate = (obj.runs / obj.balls) * 100
    else:
        obj.strike_rate = 0

    # Economy
    if obj.overs > 0:
        obj.economy = obj.runs_conceded / obj.overs
    else:
        obj.economy = 0


def calculate_player_points(obj):
    role = obj.player.role
    points = 0

    # Batting
    if role in ['Batting', 'AllRounder']:
        points += obj.runs
        points += obj.fours
        points += obj.sixes * 2

    # Bowling
    if role in ['Bowling', 'AllRounder']:
        points += obj.wickets * 25

    # Fielding
    points += obj.catches * 8

    return points


def recalculate_player_stats(player):
    from .models import  PlayerStats

    performances = PlayerMatchPerformance.objects.filter(player=player)

    stats, _ = PlayerStats.objects.get_or_create(player=player)

    stats.total_runs = performances.aggregate(Sum('runs'))['runs__sum'] or 0
    stats.total_wickets = performances.aggregate(Sum('wickets'))['wickets__sum'] or 0
    stats.total_points = performances.aggregate(Sum('total_points'))['total_points__sum'] or 0
    stats.matches = performances.count()

    stats.role = player.role

    stats.save()