from django.urls import path
from events.views import LoginView, SignupView
from . import views

urlpatterns = [
    # Path converters: int, str, path, slug, UUID
    path('', LoginView.as_view(), name="login"),
    path('my-upcoming-events', views.my_upcoming_events, name="my_upcoming_events"),
    path('home', views.home, name="home"),
    path('signup', SignupView.as_view(), name="signup"),
]