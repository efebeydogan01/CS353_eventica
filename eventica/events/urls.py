from django.urls import path
from . import views

urlpatterns = [
    # Path converters: int, str, path, slug, UUID
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('login', views.login, name="login"),
]