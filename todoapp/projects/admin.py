from django.contrib import admin

from .models import ProjectMember,Project

admin.site.register(Project)
admin.site.register(ProjectMember)
