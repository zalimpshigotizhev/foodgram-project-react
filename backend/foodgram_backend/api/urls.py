from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import DjUserViewSet

app_name = 'api'
router = DefaultRouter()

router.register("users", DjUserViewSet)

urlpatterns = (
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
)