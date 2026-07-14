from django.urls import path

from . import views

urlpatterns = [
    path("", views.qualification_list, name="qualification_list"),

    path(
        "create/",
        views.qualification_create,
        name="qualification_create",
    ),
]