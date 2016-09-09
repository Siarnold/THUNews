from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello!")

def query(request):
    return HttpResponse("query")
