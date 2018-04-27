from django.shortcuts import render

from dauditlog.views import logit, auditit
from .models import Greeting


@auditit("")
def myrender(log, request):
    return render(request, 'index.html')


# Create your views here.
@logit("")
def index(request, log):
    # return HttpResponse('Hello from Python!')
    return myrender(log, request)


def db(request, log):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
