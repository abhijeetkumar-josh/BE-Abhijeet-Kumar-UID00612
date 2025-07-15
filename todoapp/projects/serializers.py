from rest_framework import serializers

from projects.models import *
from users.models import CustomUser


class ProjectReportHelperSerializer(serializers.ModelSerializer):
    completed_count = serializers.IntegerField(read_only=True)
    pending_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'pending_count','completed_count']


class ProjectWiseReportSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='name')
    report = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['project_title', 'report']

    def get_report(self, obj):
        users = getattr(obj, 'annotated_members', [])
        return ProjectReportHelperSerializer(users, many=True).data
    