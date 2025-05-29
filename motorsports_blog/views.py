"""Views for the motorsports blog application."""

import datetime
from django.http import HttpResponse


def index(request):     # pylint: disable=unused-argument
    """Return the homepage response."""
    now = datetime.datetime.now()
    return HttpResponse(f"Hello world! The current date and time is: {now}")
