from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Project, ProjectMember

User = get_user_model()


class ProjectMemberApiViewSet(viewsets.ViewSet):
    
    permission_classes=[AllowAny]
    @action(detail=True, methods=['post'], url_path='add-users')
    def add_users(self, request, pk=None):
        
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)

        user_ids = request.data.get("user_ids", [])
        logs = {}

        current_members_count = ProjectMember.objects.filter(project=project).count()

        for user_id in user_ids:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                logs[user_id] = "User does not exist"
                continue

            user_project_count = ProjectMember.objects.filter(member=user).count()

            if user_project_count >= 2:
                logs[user_id] = "User is already in 2 projects"
                continue

            if current_members_count >= project.max_members:
                logs[user_id] = "Project has reached max members"
                continue

            if ProjectMember.objects.filter(project=project, member=user).exists():
                logs[user_id] = "User already in project"
                continue

            ProjectMember.objects.create(project=project, member=user)
            current_members_count += 1
            logs[user_id] = "User added successfully"

        # return Response({"logs": logs}, status=200)
        return Response({"logs": {str(k): v for k, v in logs.items()}}, status=200)

    @action(detail=True, methods=['put'], url_path='remove-users')
    def remove_users(self, request, pk=None):
        
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)

        user_ids = request.data.get("user_ids", [])
        logs = {}

        for user_id in user_ids:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                logs[user_id] = "User does not exist"
                continue

            try:
                membership = ProjectMember.objects.get(project=project, member=user)
                membership.delete()
                logs[user_id] = "User removed successfully"
            except ProjectMember.DoesNotExist:
                logs[user_id] = "User is not a member of this project"

        # return Response({"logs": logs}, status=200)
        return Response({"logs": {str(k): v for k, v in logs.items()}}, status=200)
    