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
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_extention = form['file'].value().name.split('.').pop()
            file_data = form['file'].value().read().decode('utf-8')
            file_data = translator.translate_file('', file_data, 'fr', file_extention)
            return HttpResponse(file_data, content_type='text/xml')
    else:
        form = UploadFileForm()
    return render(request, 'file_upload.html', {'form': form, "title": "Translate File:", "languages" : settings.LANGUAGES})


    # UploadFileForm
