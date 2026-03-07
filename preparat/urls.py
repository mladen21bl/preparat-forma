from django.urls import path
from . import views
from .views import prijava_test2, success_view, test2


urlpatterns = [
    path('', views.index, name='index'),
    path("test", prijava_test2, name="prijava_test2"),
    path("test2", test2, name="test2"),
    path("success/", success_view, name="success"),
]
