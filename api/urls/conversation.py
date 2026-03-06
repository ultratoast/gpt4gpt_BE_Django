from django.urls import path
from api.views import conversation

urlpatterns = [
    path("start", conversation.start),
    path("message", conversation.message)
]
