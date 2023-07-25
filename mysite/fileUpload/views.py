import requests
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.forms import ModelForm
from django.urls import reverse_lazy, reverse
from .forms import ImageModelForm
from .models import ImageModel
from django.contrib.auth.decorators import login_required

# Create your views here.

class DocumentCreateView(LoginRequiredMixin, FormView):
    template_name = 'fileUpload/Upload.html'
    form_class = ImageModelForm
    fid = None

    def get_success_url(self):
        return reverse('fileUpload:show', kwargs={'fid': self.fid})

    def form_valid(self, form):
        if self.request.FILES:
            form.instance.attached = self.request.FILES['files']

        item = form.save(commit=False)
        item.desc = '모델 해석 진행중'
        item.author = self.request.user
        #item.save()
        self.fid = item.pk

        response = requests.post('http://localhost:5000/predict', files = {'file':self.request.FILES['files']})
        if response.status_code == 200:
            item.desc = response.content
            item.save()
        item.save()
        self.fid = item.pk
        return super().form_valid(form)


class DocumentShowView(DetailView):
    model = ImageModel
    template_name = "fileUpload/show.html"
    pk_url_kwarg = "fid"
    context_object_name = 'fileImg'
