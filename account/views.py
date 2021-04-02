#%%
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.views.generic import TemplateView

from django.contrib.auth import logout
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

from operator import attrgetter

#%%
from account.forms import AccountCreationForm, AccountAuthenticationForm
from files.forms import ExcelForm
from files.models import ExcelDocument
from files.views import get_file_queryset
from graphs.models import AmericanStates

#%%
import os
#%%
class UploadView(CreateView):

    """
    This method allows the user to upload a file 
    """
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('landing')

        form = ExcelForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = ExcelDocument(user=request.user, upload=request.FILES['upload'])
            newdoc.user = request.user
            newdoc.save()
            context = {}
            context['form'] = ExcelForm(request.FILES)
            context['documents'] = ExcelDocument.retrieve_data(request)
            maps = []
            
            # Check if the directory is already created            
            if not os.path.exists("media/user_" + str(request.user.id) + "/maps/"):
                os.mkdir("media/user_" + str(request.user.id) + "/maps/")
            
            # Create the html map to save it
            document_name = str(newdoc).split('/')[2].split('.')[0]
            context['document_name'] = document_name
            f = open("media/user_" + str(request.user.id) + "/maps/" + document_name + ".html", "w+")
            f.write(AmericanStates("media/" + str(newdoc), document_name))
            f.close()

            # Read in the html maps 
            user_maps = os.listdir("media/user_" + str(request.user.id) + "/maps/")
            for map in user_maps:
                maps.append(open("media/user_" + str(request.user.id) + "/maps/" + map, "r").read())
            
            context['maps'] = maps
            return render(request, 'authenticated/upload.html', context)

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('landing')
        context = {}
        context['form'] = ExcelForm(request.FILES)
        context['documents'] = ExcelDocument.retrieve_data(request)
        maps = []
        # Read in the html maps 
        if os.path.exists("media/user_" + str(request.user.id)):
            user_maps = os.listdir("media/user_" + str(request.user.id) + "/maps/")
            for map in user_maps:
                maps.append(open("media/user_" + str(request.user.id) + "/maps/" + map, "r").read())

        context['maps'] = maps
        return render(request, 'authenticated/upload.html', context)

class SearchBar(ListView):
    
    model = ExcelDocument
    template_name = 'authenticated/upload.html'

    def get_queryset(self):
        queryset = []
        queries = self.request.GET.get('q')
        for q in queries:
            files = ExcelDocument.objects.filter(Q(upload__icontains=q)).distinct()
            for post in posts:
                queryset.append(files)
        return list(set(queryset))

class DeleteFile(View):

    def post(self, request, pk):
        file = ExcelDocument.objects.get(pk=pk)
        document_name = str(file).split('/')[2].split('.')[0]
        # If the user uploads a duplicate file django hashes the name and adds a extra '_' with random letters "Qr32f$a4"
        # Original unique map
        if (os.path.exists("media/user_" + str(request.user.id) + "/maps/" + document_name + ".html")):
            os.remove("media/user_" + str(request.user.id) + "/maps/" + document_name + ".html")
        # Duplicate map
        if (os.path.exists("media/user_" + str(request.user.id) + "/maps/" + str(document_name).split('_')[0] + ".html")):
            os.remove("media/user_" + str(request.user.id) + "/maps/" + str(document_name).split('_')[0] + ".html")
        
        # Original unique file
        if (os.path.exists("media/user_" + str(request.user.id) + "/files/" + document_name + ".csv")):
            os.remove("media/user_" + str(request.user.id) + "/files/" + document_name + ".csv")
        # Duplicate file
        if (os.path.exists("media/user_" + str(request.user.id) + "/files/" + str(document_name).split('_')[0] + ".csv")):
            os.remove("media/user_" + str(request.user.id) + "/files/" + str(document_name).split('_')[0] + ".csv")
        
        # Deletes file from database
        file.delete()
        return redirect('upload')
        
class Registration(View):

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('landing')

        context = {}
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('landing')
        else:
            context['registration_form'] = form
        return render(request, 'register.html', context)
    
    def get(self, request):
        context = {}
        context['registration_form'] = AccountCreationForm()
        return render(request, 'register.html', context)

class LogOut(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('landing')
        else:
            return redirect('landing')

class LogIn(View):

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('landing')
        context = {}
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('landing')
        context['signin_form'] = form
        return render(request, 'signin.html', context)
    
    def get(self, request):
        context = {}
        context['signin_form'] = AccountAuthenticationForm()
        return render(request, 'signin.html', context)


