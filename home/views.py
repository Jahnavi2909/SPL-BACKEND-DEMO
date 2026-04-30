from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Franchise  # assuming franchise = Team
from core.models import Player
from matches.models import Match

from .serializers import DashboardSerializer


class DashboardView(APIView):

    def get(self, request):
        data = {
            "franchise_count": Franchise.objects.count(),
            "player_count": Player.objects.count(),
            "match_count": Match.objects.count(),
        }

        serializer = DashboardSerializer(data)
        return Response(serializer.data)
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAdmin
from django.contrib.admin.models import LogEntry

from .serializers import RecentActivitySerializer


class RecentActivitiesAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        activities = LogEntry.objects.select_related(
            'user', 'content_type'
        ).order_by('-action_time')[:20]

        serializer = RecentActivitySerializer(activities, many=True)
        return Response(serializer.data)
    def get_change_message(self, obj):
        try:
            import json
            return json.loads(obj.change_message)
        except:
            return obj.change_message
