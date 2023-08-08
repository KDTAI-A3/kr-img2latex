from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "fileUpload"

urlpatterns = [
    path("", TemplateView.as_view(template_name='fileUpload/Main.html'), name="index"),
    path("help", TemplateView.as_view(template_name='fileUpload/Help.html'), name="help"),
    
    path("upload", views.DocumentCreateView.as_view(), name="upload"),
    path("show/<int:fid>", views.DocumentShowView.as_view(), name="show"),
    path("list", views.DocumentListView.as_view(), name="list"),
    path("getLatex/<int:fid>", views.GetExtractView.as_view(), name="getLatex"),
    path("getCls/<int:fid>", views.GetClassifyResultView.as_view(), name="getCls"),
    path("doChatGpt/<int:fid>", views.ChatGptResultView.as_view(), name="doChatGpt"),
    path('getLatexText', views.GetLatexData, name='getLatexText'),
    path('getGPTText', views.GetGPTData, name='getGPTText'),
]
