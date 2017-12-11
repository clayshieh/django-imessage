from django.conf import settings
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from messages.models import Message, Handle

from datetime import datetime, timedelta
from pytz import timezone


def index(request, template_name="messages/index.html"):

    context = {
        "handles": Handle.objects.all()
    }

    return render_to_response(template_name,
            RequestContext(request, context))


def messages(request, handle_id, template_name="messages/messages.html"):

    handle = Handle.objects.get(pk=handle_id)

    messages = []
    if "filter" in request.GET:
        app_tz = timezone(settings.TIME_ZONE)
        start_date = datetime.strptime(request.GET["filter"], "%Y-%m-%d").replace(tzinfo=app_tz)
        end_date = start_date + timedelta(days=1)
        for message in handle.message_set.all():
            msg_date = message.date
            if msg_date < start_date:
                continue
            elif msg_date > end_date:
                break
            else:
                messages.append(message)
    else:
        messages = handle.message_set.all()

    context = {
        "handle": handle,
        "messages": messages,
    }

    return render(request, template_name, context)

