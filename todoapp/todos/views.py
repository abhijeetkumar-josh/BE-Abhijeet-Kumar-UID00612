from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Todo
from .serializers import (Todo_Create_Serializer, Todo_Detail_Serializer,
                          Todo_List_Serializer, Todo_Update_Serializer)


class TodoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class IsOwner(BasePermission):
    
    def has_object_permission(self,request,view,obj):
      return obj.user==request.user

class TodoAPIViewSet(viewsets.ViewSet):
    """
    Handles Create, Update, Get, Delete and List operations for Todo.
    """
    permission_classes =    [IsAuthenticated & IsOwner]
    authentication_classes= [TokenAuthentication]
    # permission_classes=     [AllowAny]
    pagination_class = TodoPagination


    def create(self, request):
        serializer = Todo_Create_Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = serializer.save()
        return Response({
            "todo": todo.name,
            "done": todo.done,
            "Date_created": todo.date_created,
            'id':todo.id
        })
       
    @action(detail=False, methods=['put'], url_path='update')
    def update_todo(self, request):
        try:
            todo = Todo.objects.get(id=request.data.get("todo_id"))
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found"}, status=404)
        self.check_object_permissions(request, todo)
        serializer = Todo_Update_Serializer(todo, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    def retrieve(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"error": "Todo not found"}, status=404)
        self.check_object_permissions(request, todo)
        serializer = Todo_Detail_Serializer(todo)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            todo = Todo.objects.get(pk=pk)
            self.check_object_permissions(request, todo)
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
        self.check_object_permissions(request, todos)
        paginator = self.pagination_class()
        paginated_qs = paginator.paginate_queryset(todos, request)
        serializer = Todo_List_Serializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)
