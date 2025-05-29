"""Views for the motorsports blog application."""

import datetime
from django.http import HttpResponse


def index(request):
    now = datetime.datetime.now()
    # Return the home page response.
    return HttpResponse(f"Hello world! The current date and time is: {now}")
