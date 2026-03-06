from django.urls import path, include

urlpatterns = [
    path("conversation/", include("api.urls.conversation"))
]
