from django.urls import path

from apps.common.views import live

urlpatterns = [path("health/live", live, name="health-live")]
