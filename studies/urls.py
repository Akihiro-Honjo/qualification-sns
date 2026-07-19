from django.urls import path

from . import views

urlpatterns = [
    path(
        "<int:qualification_id>/",
        views.study_record_list,
        name="study_record_list",
    ),
    path(
    "<int:qualification_id>/create/",
    views.study_record_create,
    name="study_record_create",
    ),
]