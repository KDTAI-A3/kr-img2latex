from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.forms import ModelForm
from django.urls import reverse_lazy, reverse
from .forms import ImageModelForm
from .models import ImageModel
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import ListView, RedirectView
from uuid import uuid4
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator

from .api import sendImageAPI, imgToLatexAPI, classifyLatexAPI, chatgptAPI
# Create your views here.

from requests.compat import (
    Mapping,
    basestring,
    bytes,
    getproxies,
    getproxies_environment,
    integer_types,
)







class DocumentCreateView(LoginRequiredMixin, FormView):
    template_name = 'fileUpload/UploadFile.html'
    form_class = ImageModelForm
    fid = None

    def get_success_url(self):
        return reverse('fileUpload:show', kwargs={'fid': self.fid})

    def form_valid(self, form):
        if self.request.FILES:
            form.instance.attached = self.request.FILES['files']

        item = form.save(commit=False)
        #item.result = '모델 해석 진행중'
        item.author = self.request.user
        item.create_date = timezone.now()
        #item.save()
        self.fid = item.pk
        is_success, modelserver_img_no, _ = sendImageAPI(self.request.FILES['files'],timestamp=item.create_date)
        
        if is_success:
            item.modelserver_img_no = modelserver_img_no
            item.save()
            self.fid = item.pk
            return super().form_valid(form)
        #print(response.text)
        return JsonResponse({'error':modelserver_img_no})


class DocumentShowView(DetailView):
    model = ImageModel
    template_name = "fileUpload/show.html"
    pk_url_kwarg = "fid"
    context_object_name = 'fileImg'

class DocumentListView(LoginRequiredMixin, ListView):
    model = ImageModel
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data()
        
        page = context['page_obj']
        paginator = page.paginator
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=3, on_ends=0)
        context['pagelist'] = pagelist
         
        return context
    
    def get_queryset(self):
        return ImageModel.objects.filter(author = self.request.user)
    context_object_name = "imgList"
    template_name="fileUpload/list.html"

class GetExtractView(LoginRequiredMixin, RedirectView):
    def get(self,request, *args, **kwargs):

        fid = kwargs['fid']
        fileObj = ImageModel.objects.get(id = fid)
        if fileObj.author.id != self.request.user.id:
            return HttpResponse(status=401)
        if fileObj.modelserver_img_no is None:
            return HttpResponse(status=500)
        
        if fileObj.is_text_extracted == False:
            is_success, result, _ = imgToLatexAPI(fileObj.modelserver_img_no)
            if is_success:
                fileObj.extracted_texts = result
                fileObj.is_text_extracted = True
                fileObj.save()
            else:
                return HttpResponse(status=500)
        return redirect(reverse_lazy("fileUpload:show",kwargs = {'fid':fid}))
        
class GetClassifyResultView(LoginRequiredMixin, RedirectView):
    def get(self,request, *args, **kwargs):

        fid = kwargs['fid']
        fileObj = ImageModel.objects.get(id = fid)
        if fileObj.author.id != self.request.user.id:
            return HttpResponse(status=401)
        if fileObj.modelserver_img_no is None:
            return HttpResponse(status=500)
        if fileObj.is_level_classified == False:
            is_success, result, _ = classifyLatexAPI(fileObj.modelserver_img_no)
            if len(result)>1000:
                result = result[:1000]
            if is_success:
                fileObj.classified_level = str(result)
                fileObj.is_level_classified = True
                fileObj.save()
            else:
                return HttpResponse(status=500)
            
        return redirect(reverse_lazy("fileUpload:show",kwargs = {'fid':fid}))

class ChatGptResultView(LoginRequiredMixin, RedirectView):
    def get(self,request, *args, **kwargs):

        fid = kwargs['fid']
        fileObj = ImageModel.objects.get(id = fid)
        if fileObj.author.id != self.request.user.id:
            return HttpResponse(status=401)
        if fileObj.is_chatgpt_analyzed == False:

            result = str(chatgptAPI(fileObj.extracted_texts))
            if len(result)>4096:
                result = result[:4096]
            is_success = True
            if is_success:
                fileObj.chatgpt_result = result
                fileObj.is_chatgpt_analyzed = True
                fileObj.save()
            else:
                return HttpResponse(status=500)
            
        return redirect(reverse_lazy("fileUpload:show",kwargs = {'fid':fid}))

def GetLatexData(request):
    fid = request.GET.get('id', None)
    fileObj = ImageModel.objects.get(id = fid)

    jsonData = {'value':fileObj.extracted_texts}

    return JsonResponse(jsonData)

def GetGPTData(request):
    fid = request.GET.get('id', None)
    fileObj = ImageModel.objects.get(id = fid)

    jsonData = {'value':fileObj.chatgpt_result}

    return JsonResponse(jsonData)