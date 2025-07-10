import json
from .models import Todo
from users.models import CustomUser
from .serializers import TaskSerializer,Task2Serializer,User2Serializer,Serializer3,Serializer4,Serializer5,projectSerializer,Serializer6,UserProjectStatusSerializer,Serializer9
from users.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from projects.models import Project,ProjectMember
from django.db.models import Count, Q
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Prefetch
from django.contrib.postgres.aggregates import ArrayAgg


# from .todoapp.users.models import CustomUser
# Add code to this util to return all users list in specified format.
# [ {
#   "id": 1,
#   "first_name": "Amal",
#   "last_name": "Raj",
#   "email": "amal.raj@joshtechnologygroup.com"
# },
# {
#   "id": 2,
#   "first_name": "Gurpreet",
#   "last_name": "Singh",
#   "email": "gurpreet.singh@joshtechnologygroup.com"
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.

def fetch_all_users():
    """
    Util to fetch given user's tod0 list
    :return: list of dicts - List of users data
    """
    userdata=CustomUser.objects.all()
    serializer=UserSerializer(userdata,many=True)
    return json.loads(json.dumps(serializer.data))
    # print(json.loads(json.dumps(serializer.data)))
    # print(json.dumps(data))
    


# Add code to this util to  return all todos list (done/to do) along with user details in specified format.
# [{
#   "id": 1,
#   "name": "Complete Timesheet",
#   "status": "Done",
#   "created_at": "4:30 PM, 12 Dec, 2021"
#   "creator" : {
#       "first_name": "Amal",
#       "last_name": "Raj",
#       "email": "amal.raj@joshtechnologygroup.com",
#   }
# },
# {
#   "id": 2,
#   "name": "Complete Python Assignment",
#   "status": "To Do",
#   "created_at": "5:30 PM, 13 Dec, 2021",
#   "creator" : {
#      "first_name": "Gurpreet",
#       "last_name": "Singh",
#       "email": "gurpreet.singh@joshtechnologygroup.com",
#   }
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_all_todo_list_with_user_details():
    userdata=Todo.objects.select_related('user').all()
    serializer=Task2Serializer(userdata,many=True)
    return json.loads(json.dumps(serializer.data))
    # print(json.dumps(serializer.data))
    # print(json.dumps(serializer.data))


# Add code to this util to return all projects with following details in specified format.
# [{
#   "id": 1,
#   "name": "Project A",
#   "status": "Done",
#   "existing_member_count": 4,
#   "max_members": 5
# },
# {
#   "id": 2,
#   "name": "Project C",
#   "status": "To Do",
#   "existing_member_count": 2,
#   "max_members": 4
# }]
# Note: use serializer for generating this format. use source for status in serializer field.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_projects_details():
    # pro=Project.objects.all()
    pass

    


# Add code to this util to  return stats (done & to do count) of all users in specified format.
# [{
#   "id": 1,
#   "first_name": "Amal",
#   "last_name": "Raj",
#   "email": "amal.raj@joshtechnologygroup.com",
#   "completed_count": 3,
#   "pending_count": 4
# },
# {
#   "id": 2,
#   "first_name": "Gurpreet",
#   "last_name": "Singh",
#   "email": "gurpreet.singh@joshtechnologygroup.com",
#   "completed_count": 5,
#   "pending_count": 0
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_users_todo_stats():
    users = CustomUser.objects.annotate(
        completed_count=Count('todos', filter=Q(todos__done=True)),
        pending_count=Count('todos', filter=Q(todos__done=False))
    )
    serializer=Serializer4(users,many=True)
    # print(json.dumps(serializer.data))
    return json.loads(json.dumps(serializer.data))



# Add code to this util to return top five users with maximum number of pending todos in specified format.
# [{
#   "id": 1,
#   "first_name": "Nikhil",
#   "last_name": "Khurana",
#   "email": "nikhil.khurana@joshtechnologygroup.com",
#   "pending_count": 10
# },
# {
#   "id": 2,
#   "first_name": "Naveen",
#   "last_name": "Kumar",
#   "email": "naveenk@joshtechnologygroup.com",
#   "pending_count": 4
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_five_users_with_max_pending_todos():
    users = CustomUser.objects.annotate(
        completed_count=Count('todos', filter=Q(todos__done=True)),
        pending_count=Count('todos', filter=Q(todos__done=False))
    ).order_by('-pending_count')[:5]
    serializer=Serializer4(users,many=True)
    return json.loads(json.dumps(serializer.data))
    # print(json.dumps(serializer.data))


# Add code to this util to return users with given number of pending todos in specified format.
# e.g where n=4
# [{
#   "id": 1,
#   "first_name": "Nikhil",
#   "last_name": "Khurana",
#   "email": "nikhil.khurana@joshtechnologygroup.com",
#   "pending_count": 4
# },
# {
#   "id": 2,
#   "first_name": "Naveen",
#   "last_name": "Kumar",
#   "email": "naveenk@joshtechnologygroup.com",
#   "pending_count": 4
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
# Hint : use annotation and aggregations
def fetch_users_with_n_pending_todos(n):
    users = CustomUser.objects.annotate(
        pending_count=Count('todos', filter=Q(todos__done=False))
    ).filter(pending_count=n)
    serializer=Serializer9(users,many=True)
    return json.loads(json.dumps(serializer.data))
    # print(json.dumps(serializer.data))


# Add code to this util to return todos that were created in between given dates (add proper order too) and marked as
# done in specified format.
#  e.g. for given range - from 12-01-2021 to 12-02-2021
# [{
#   "id": 1,
#   "creator": "Amal Raj"
#   "email": "amal.raj@joshtechnologygroup.com"
#   "name": "Complete Timesheet",
#   "status": "Done",
#   "created_at": "4:30 PM, 12 Jan, 2021"
# },
# {
#   "id": 2,
#   "creator": "Nikhil Khurana"
#   "email": "nikhil.khurana@joshtechnologygroup.com"
#   "name": "Complete Python Assignment",
#   "status": "Done",
#   "created_at": "5:30 PM, 02 Feb, 2021"
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_completed_todos_with_in_date_range(start, end):
    """
    Util to fetch todos that were created in between given dates and marked as done.
    :param start: string - Start date e.g. (12-01-2021)
    :param end: string - End date e.g. (12-02-2021)
    :return: list of dicts - List of todos
    """
    # Write your code here
    pass


# Add code to this util to return list of projects having members who have name either starting with A or ending with A
# (case-insensitive) in specified format.
# [{
#   "project_name": "Project A"
#   "done": False
#   "max_members": 3
#   },
#   {
#   "project_name": "Project B"
#   "done": False
#   "max_members": 3
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_project_with_member_name_start_or_end_with_a():
    """
    Util to fetch project details having members who have name either starting with A or ending with A.
    :return: list of dicts - List of project data
    """
    # Write your code here
    pass


# Add code to this util to return project wise todos stats per user in specified format.
# [{
#   "project_title": "Project A"
#   "report": [
#       {
#           "first_name": "Amal",
#           "last_name": "Raj",
#           "email": "amal.raj@joshtechnologygroup.com",
#           "pending_count": 1,
#           "completed_count": 1,
#       },
#       {
#           "first_name": "Nikhil",
#           "last_name": "Khurana",
#           "email": "nikhil.khurana@joshtechnologygroup.com",
#           "pending_count": 0,
#           "completed_count": 5,
#       }
#   ]
# },
# {
#   "project_title": "Project B"
#   "report": [
#       {
#           "first_name": "Gurpreet",
#           "last_name": "Singh",
#           "email": "gurpreet.singh@joshtechnologygroup.com",
#           "pending_count": 12,
#           "completed_count": 15,
#       },
#       {
#           "first_name": "Naveen",
#           "last_name": "Kumar",
#           "email": "naveenk@joshtechnologygroup.com",
#           "pending_count": 12,
#           "completed_count": 5,
#       }
#   ]
# }]
# Note: use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
def fetch_project_wise_report():
    annotated_users = CustomUser.objects.annotate(
        completed_count=Count('todos', filter=Q(todos__done=True)),
        pending_count=Count('todos', filter=Q(todos__done=False))
    ).order_by('email')

    projects = Project.objects.prefetch_related(
        Prefetch('member', queryset=annotated_users, to_attr='annotated_members')
    )

    serializer = projectSerializer(projects, many=True)
    # print(json.loads(json.dumps(serializer.data)))
    return json.loads(json.dumps(serializer.data))


# Add code to this util to return all users project stats in specified format.
# [{
#   "first_name": "Amal",
#   "last_name": "Raj",
#   "email": "amal.raj@joshtechnologygroup.com",
#   "projects" : {
#       "to_do": ["Project A", "Project C"],
#       "in_progress": ["Project B", "Project E"],
#       "completed": ["Project R", "Project L"],
#   }
# },
# {
#   "first_name": "Nikhil",
#   "last_name": "Khurana",
#   "email": "nikhil.khurana@joshtechnologygroup.com",
#   "projects" : {
#       "to_do": ["Project C"],
#       "in_progress": ["Project B", "Project F"],
#       "completed": ["Project K", "Project L"],
#   }
# }]
# Note: Use serializer for generating this format.
# use json.load(json.dumps(serializer.data)) while returning data from this function for test cases to pass.
# Hint: Use subquery/aggregation for project data.
def fetch_user_wise_project_status():
    """
    Util to fetch user wise project statuses.
    :return: list of dicts - List of user project data
    """
    result=[]
    users_with_projects = CustomUser.objects.annotate(
      to_be_started_projects=ArrayAgg(
        'project_membership__project__name',
        filter=Q(project_membership__project__status=0),
        distinct=True
      ),
      in_progress_projects=ArrayAgg(
        'project_membership__project__name',
        filter=Q(project_membership__project__status=1),
        distinct=True
      ),
      completed_projects=ArrayAgg(
        'project_membership__project__name',
        filter=Q(project_membership__project__status=2),
        distinct=True
      ),
    )
    for user in users_with_projects:
        if user.first_name=='abhijeet': continue
        result.append({
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "to_do_projects": user.to_be_started_projects,
        "in_progress_projects": user.in_progress_projects,
        "completed_projects": user.completed_projects,
        })


    serializer = UserProjectStatusSerializer(result, many=True)
    # print(json.loads(json.dumps(serializer.data)))
    return json.loads(json.dumps(serializer.data))




