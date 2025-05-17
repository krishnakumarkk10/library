from django.contrib import admin
from django.urls import path
from accounts.views import (
    CreateRecoreView,
    UpdateRecordView,
    DeleteRecordView,
    GetRecordsView,
)

urlpatterns = [
    path("create_record/", CreateRecoreView.as_view(), name="create_record"),
    path(
        "update_record/",
        UpdateRecordView.as_view(),
        name="update_record",
    ),
    path(
        "delete_record/",
        DeleteRecordView.as_view(),
        name="delete_record",
    ),
    path("get_records/", GetRecordsView.as_view(), name="get_records"),
]
