from django.urls import path
from . import views
from .views import prijava_test2, success_view


urlpatterns = [
    path('', views.index, name='index'),
    path("test", prijava_test2, name="prijava_test2"),
    path("success/", success_view, name="success"),
]
