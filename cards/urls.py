from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.card_list, name="card_list"),
    path("create/", views.create, name="create"),
    path("add/", views.add, name="add"),
    path("search/", views.search, name="search"),
    path("results/", views.results, name="results"),
    path("<str:name>/", views.edit, name="edit"),
    path("<str:name>/update", views.update, name="update"),
    path("<str:name>/delete", views.delete, name="delete"),
]