from django.urls import path
from . import views
from .views import BiljniDodatakCreateView


urlpatterns = [
    path('', views.index, name='index'),
    path("test/", BiljniDodatakCreateView.as_view(), name="test"),
    path('test2/', views.test2, name='test2'),
]
