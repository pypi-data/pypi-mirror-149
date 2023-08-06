from django.urls import path

from labeltree import views

urlpatterns = [
    path("list/", views.list, name="list"),
]
