from django.urls import path
from . import views

urlpatterns = [
    # Path converters: int, str, path, slug, UUID
    path('my-upcoming-events', views.my_upcoming_events, name="my_upcoming_events"),
]