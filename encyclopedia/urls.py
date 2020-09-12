from django.urls import path 
from . import views

urlpatterns = [
  path("", views.index, name='index'),
  path("wiki/<str:entry_id>", views.entry, name='entry'),
  path("wiki/action/random/", views.random_page, name='random_page'),
  path("wiki/action/newpage/", views.newpage, name='newpage'),
  path("wiki/action/edit/<str:entry_id>", views.edit, name='edit'),
  path("wiki/action/edit", views.savedit, name='savedit'),
  path("wiki/action/remove/<str:entry_id>", views.remove, name='remove'),
  path("search/<str:term>", views.search, name='search'),
  path("login", views.login_view, name='login'),
  path("logout", views.logout_view, name='logout'),
  path("register", views.register, name='register'),
  path("readme", views.readme, name='readme')
]