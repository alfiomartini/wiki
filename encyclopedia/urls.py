from django.urls import path 
from . import views

urlpatterns = [
  path("", views.index, name='index'),
  path("wiki/<str:entry_id>", views.entry, name='entry'),
  path("wiki/random/", views.random_page, name='random_page')
]