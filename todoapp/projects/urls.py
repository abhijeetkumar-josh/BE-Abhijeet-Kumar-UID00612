from rest_framework.routers import DefaultRouter

from .views import ProjectMemberApiViewSet

router = DefaultRouter()
router.register(r'manage', ProjectMemberApiViewSet, basename='manage')
urlpatterns = router.urls
