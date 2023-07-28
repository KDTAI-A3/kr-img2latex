from django.urls import path

from . import views

app_name = "fileUpload"

urlpatterns = [
    path("", views.DocumentCreateView.as_view(), name="index"),
    path("upload", views.DocumentCreateView.as_view(), name="upload"),
    path("show/<int:fid>", views.DocumentShowView.as_view(), name="show"),
    path("list", views.DocumentListView.as_view(), name="list"),
    path("getLatex/<int:fid>", views.GetExtractView.as_view(), name="getLatex"),
    path("getCls/<int:fid>", views.GetClassifyResultView.as_view(), name="getCls"),
]
