from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('newSearch', views.new_search, name="NewSearch")
]
