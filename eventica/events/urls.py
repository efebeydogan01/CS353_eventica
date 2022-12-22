from django.urls import path
from events.views import LoginView, SignupView
from . import views

urlpatterns = [
    # Path converters: int, str, path, slug, UUID
    path('', LoginView.as_view(), name="login"),
    path('home', views.home, name="home"),
    path('signup', SignupView.as_view(), name="signup"),
    path('create-event', views.create_event, name="create_event"),
]