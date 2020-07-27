from django.urls import path 
from . import views

urlpatterns = [
  path("", views.index, name='index'),
  path("wiki/<str:entry_id>", views.entry, name='entry'),
  path("wiki/r/random/", views.random_page, name='random_page'),
  path("wiki/n/newpage/", views.newpage, name='newpage'),
  path("wiki/edit/<str:entry_id>", views.edit, name='edit'),
  path("wiki/s/edit", views.savedit, name='savedit'),
  path("search/<str:term>", views.search, name='search'),
  path("login", views.login_view, name='login'),
  path("logout", views.logout_view, name='logout')
]