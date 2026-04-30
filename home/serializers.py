from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    franchise_count = serializers.IntegerField()
    player_count = serializers.IntegerField()
    match_count = serializers.IntegerField()

from rest_framework import serializers
from django.contrib.admin.models import LogEntry

class RecentActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    content_type = serializers.StringRelatedField()
    action = serializers.SerializerMethodField()

    class Meta:
        model = LogEntry
        fields = [
            'id',
            'user',
            'content_type',
            'object_repr',
            'action',
            'change_message',
            'action_time'
        ]

    def get_action(self, obj):
        if obj.action_flag == 1:
            return "Added"
        elif obj.action_flag == 2:
            return "Updated"
        elif obj.action_flag == 3:
            return "Deleted"
        return "Unknown"