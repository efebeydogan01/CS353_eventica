from django.urls import path
from . import views

urlpatterns = [
    # Path converters: int, str, path, slug, UUID
    path('', views.home, name="home"),
    path('my-upcoming-events', views.my_upcoming_events, name="my_upcoming_events"),
    path('login', views.login, name="login"),
]