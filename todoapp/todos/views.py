from rest_framework.viewsets import ModelViewSet
# from rest_framework.response import Response
# from .models import Todo
# from .serializers import TodoCreateSerializer
# from rest_framework.permissions import AllowAny
# from rest_framework import status

# class TodoAPIViewSet(ModelViewSet):
#     """
#         success response for create/update/get
#         {
#           "name": "",
#           "done": true/false,
#           "date_created": ""
#         }

#         success response for list
#         [
#           {
#             "name": "",
#             "done": true/false,
#             "date_created": ""
#           }
#         ]
#     """



# views.py
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from .models import Todo
from .serializers import (
    TodoCreateSerializer,
    TodoUpdateSerializer,
    TodoDetailSerializer,
    TodoListSerializer
)
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action


class TodoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class TodoAPIViewSet(viewsets.ViewSet):
    """
    Handles Create, Update, Get, Delete and List operations for Todo.
    """
    permission_classes = [AllowAny]
    pagination_class = TodoPagination


    def create(self, request):
        serializer = TodoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = serializer.save()
        return Response({
            "todo": todo.name,
            "done": todo.done,
            "Date_created": todo.date_created,
        })
       
    @action(detail=False, methods=['put'], url_path='update')
    def update_todo(self, request):
        try:
            todo = Todo.objects.get(id=request.data.get("todo_id"))
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found"}, status=404)

        serializer = TodoUpdateSerializer(todo, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    def retrieve(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found"}, status=404)
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found"}, status=404)

    @action(detail=False, methods=['get'], url_path='list')
    def list_user_todos(self, request):
        user_id = id=request.data.get("user_id")
        if not user_id:
            return Response({"error": "user_id is required"}, status=400)
        todos = Todo.objects.filter(user_id=user_id).order_by('-date_created')
        paginator = self.pagination_class()
        paginated_qs = paginator.paginate_queryset(todos, request)
        serializer = TodoListSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)




