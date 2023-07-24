from django.urls import path

from . import views

app_name = "fileUpload"

urlpatterns = [
    path("", views.DocumentCreateView.as_view(), name="index"),
    path("show/<int:fid>", views.DocumentShowView.as_view(), name="show")
]
