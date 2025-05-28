from django.http import HttpResponse
import datetime

def index(request):
    now = datetime.datetime.now()
    return HttpResponse(f"Hello world! The current date and time is: {now}")
