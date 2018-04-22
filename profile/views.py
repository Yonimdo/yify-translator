from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

import translator
from lenguatranslator import settings
from .forms import SignUpForm, UploadFileForm
from django.http import HttpResponse

xml_pattern = r'\<(.+)\>(.+)\<\/(.+)\>'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, "title": "Sign up"})


@login_required()
def translate_file(request):
    if request.method == 'POST':
        lanugages = request.POST.getlist('languages[]')
        file = request.FILES['file']
        file_extention = file.name.split('.').pop()
        file_data = file.read().decode('utf-8')
        file_data = translator.translate_file('', file_data, 'fr', file_extention)
        return HttpResponse(file_data, content_type='text/xml')
    else:
        return render(request, 'file_upload.html', {"title": "Translate File:", "languages": settings.LANGUAGES})


    # UploadFileForm
