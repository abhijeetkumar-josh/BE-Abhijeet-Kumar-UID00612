from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Todo
from users.models import CustomUser
from projects.models import *
from django.db.models import Count, Q
import json

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Todo
        fields='__all__'

class User2Serializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email']

class Task2Serializer(serializers.ModelSerializer):
    creator=User2Serializer(source='user',read_only=True)
    created_at = serializers.DateTimeField(source='date_created', format='%I:%M %p, %d %b, %Y')
    status=serializers.ReadOnlyField()
    class Meta:
        model=Todo
        fields=['id','name','status','created_at','creator']

    
class Serializer3(serializers.ModelSerializer):
    user=User2Serializer(many=True,read_only=True)
    class Meta:
        model=Project
        fields=['id','name','max_member','status']


class Serializer4(serializers.ModelSerializer):
    completed_count=serializers.IntegerField(read_only=True)
    pending_count=serializers.IntegerField(read_only=True)
    class Meta:
        model=CustomUser
        fields=['id','first_name','last_name','email','completed_count','pending_count']
class Serializer9(serializers.ModelSerializer):
    # completed_count=serializers.IntegerField(read_only=True)
    pending_count=serializers.IntegerField(read_only=True)
    class Meta:
        model=CustomUser
        fields=['id','first_name','last_name','email','pending_count']

    
class Serializer5(serializers.ModelSerializer):
    completed_count = serializers.IntegerField(read_only=True)
    pending_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'pending_count','completed_count']

class projectSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='name')
    report = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['project_title', 'report']

    def get_report(self, obj):
        # Use the prefetched and annotated users stored in `annotated_members`
        users = getattr(obj, 'annotated_members', [])
        return Serializer5(users, many=True).data
    
class Serializer6(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['name','max_members']


class UserProjectStatusSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    to_do_projects = serializers.ListField(child=serializers.CharField())
    in_progress_projects = serializers.ListField(child=serializers.CharField())
    completed_projects = serializers.ListField(child=serializers.CharField())


# class TodoSerializer(serializers.ModelSerializer):
#     created_at = serializers.DateTimeField(source='date_created', format='%I:%M %p, %d %b, %Y',read_only=True)
#     class Meta:
#         model=Todo
#         fields=['id','name','status','created_at','done']
#         read_only_fields=['id','created_at']
    



# class TodoSerializer(serializers.ModelSerializer):
#     user_id = serializers.IntegerField(write_only=True)


class TodoCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    todo = serializers.CharField(source='name')

    class Meta:
        model = Todo
        fields = ['user_id','todo', 'done', 'date_created']
        read_only_fields = ['done', 'date_created']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = CustomUser.objects.get(id=user_id)
        return Todo.objects.create(user=user, **validated_data)


class TodoUpdateSerializer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source='id')
    todo =serializers.CharField(source='name')
    class Meta:
        model = Todo
        fields = ['todo_id', 'todo', 'done']


class TodoDetailSerializer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source='id')
    todo =serializers.CharField(source='name')
    class Meta:
        model = Todo
        fields = ['todo_id', 'todo', 'done']



class TodoListSerializer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source='id')
    todo =serializers.CharField(source='name')
    class Meta:
        model = Todo
        fields = ['todo_id', 'todo', 'done', 'date_created']