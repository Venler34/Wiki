from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.getEntry, name="getEntry"),
    path("new", views.newPage, name="newPage"),
    path("edit/<str:title>", views.editPage, name="editPage"),
    path("random", views.randomPage, name="randomPage")
]
