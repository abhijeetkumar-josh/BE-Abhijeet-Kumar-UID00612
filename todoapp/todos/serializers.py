import json

from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from rest_framework import serializers

from projects.models import *
from users.models import CustomUser

from .models import Todo


class nested_Serializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email']


class all_todos_Serializer(serializers.ModelSerializer):
    creator=nested_Serializer(source='user',read_only=True)
    created_at = serializers.DateTimeField(source='date_created', format='%I:%M %p, %d %b, %Y')
    status=serializers.ReadOnlyField()
    class Meta:
        model=Todo
        fields=['id','name','status','created_at','creator']


class users_todo_stats_Serializer(serializers.ModelSerializer):
    completed_count=serializers.IntegerField(read_only=True)
    pending_count=serializers.IntegerField(read_only=True)
    class Meta:
        model=CustomUser
        fields=['id','first_name','last_name','email','completed_count','pending_count']


class pending_todos_Serializer(serializers.ModelSerializer):
    pending_count=serializers.IntegerField(read_only=True)
    class Meta:
        model=CustomUser
        fields=['id','first_name','last_name','email','pending_count']

    
class project_report_helper_Serializer(serializers.ModelSerializer):
    completed_count = serializers.IntegerField(read_only=True)
    pending_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'pending_count','completed_count']


class project_wise_report_Serializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='name')
    report = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['project_title', 'report']

    def get_report(self, obj):
        users = getattr(obj, 'annotated_members', [])
        return project_report_helper_Serializer(users, many=True).data


class user_wise_project_status_Serializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    to_do_projects = serializers.ListField(child=serializers.CharField())
    in_progress_projects = serializers.ListField(child=serializers.CharField())
    completed_projects = serializers.ListField(child=serializers.CharField())


class Todo_Create_Serializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    todo = serializers.CharField(source='name')

    class Meta:
        model = Todo
        fields = ['user_id','todo', 'done', 'date_created','id']
        read_only_fields = ['done', 'date_created']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = CustomUser.objects.get(id=user_id)
        return Todo.objects.create(user=user, **validated_data)


class Todo_Update_Serializer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source='id')
    todo =serializers.CharField(source='name')
    class Meta:
        model = Todo
        fields = ['todo_id', 'todo', 'done']


class Todo_Detail_Serializer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source='id')
    todo =serializers.CharField(source='name')
    class Meta:
        model = Todo
        fields = ['todo_id', 'todo', 'done']


class Todo_List_Serializer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source='id')
    todo =serializers.CharField(source='name')
    class Meta:
        model = Todo
        fields = ['todo_id', 'todo', 'done', 'date_created']
