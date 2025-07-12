from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

api_urls = [
    path('todos/', include('todos.urls')),
    path('', include('users.urls')),
    path('manage/',include('projects.urls'))
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('api/token-auth/', obtain_auth_token),
]
