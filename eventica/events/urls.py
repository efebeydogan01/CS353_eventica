from django.urls import path
from events.views import LoginView, SignupView, LogoutView
from . import views

urlpatterns = [
    # Path converters: int, str, path, slug, UUID
    path('', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('home', views.home, name="home"),
    path('signup', SignupView.as_view(), name="signup"),
    path('create-event', views.create_event, name="create_event"),
    path('my-events', views.my_events, name="my_events"),
    path('edit-event', views.edit_event, name="edit_event"),
    path('reports', views.reports, name="reports"),
    path('artists', views.artists, name="artists"),
]