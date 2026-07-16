from django.urls import path

from . import views

urlpatterns = [
    path("", views.qualification_list, name="qualification_list"),

    path(
        "create/",
        views.qualification_create,
        name="qualification_create",
    ),
    
    path(
    "<int:pk>/edit/",
    views.qualification_update,
    name="qualification_update",
    ),
    
    path(
    "<int:pk>/delete/",
    views.qualification_delete,
    name="qualification_delete",
),
]