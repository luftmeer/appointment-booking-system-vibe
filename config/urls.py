from django.urls import include, path

urlpatterns = [path("", include("apps.common.urls"))]
