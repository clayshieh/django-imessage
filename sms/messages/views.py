from django.conf import settings
from django.shortcuts import render

from messages.models import Message, Handle

from datetime import datetime, timedelta
from pytz import timezone


def index(request):

    context = {
        "handles": Handle.objects.all()
    }

    return render(request, "messages/index.html", context)


def messages(request, handle_id):

    handle = Handle.objects.get(pk=handle_id)

    # filtering functions
    start_date = None
    end_date = None
    search_terms_cleaned = []

    if "filter" in request.GET:
        if request.GET["filter"]:
            app_tz = timezone(settings.TIME_ZONE)
            start_date = datetime.strptime(request.GET["filter"], "%Y-%m-%d").replace(tzinfo=app_tz)
            end_date = start_date + timedelta(days=1)

    if "search" in request.GET:
        print request.GET["search"]
        if request.GET["search"]:
            query = request.GET["search"].upper()
            if query:
                search_terms = []
                if " OR " in query:
                    for q in query.split(" OR "):
                        search_terms.append([q.strip()])
                else:
                    search_terms.append([query])
                for search_term in search_terms:
                    tmp = []
                    if " AND " in search_term[0]:
                        for x in search_term[0].split(" AND "):
                            tmp.append(x.strip())
                    else:
                        tmp = search_term
                    search_terms_cleaned.append(tmp)

    messages = handle.message_set.all()

    def valid_date(message):
        msg_date = message.date
        if msg_date < start_date:
            return 0
        elif msg_date > end_date:
            return -1
        else:
            return 1

    def valid_search(message):
        message_text = message.text.upper()
        for search_term in search_terms_cleaned:
            if len(search_term) == 1:
                if search_term[0] in message_text:
                    return True
            else:
                found = True
                for search_term_mul in search_term:
                    if not found:
                        break
                    else:
                        found = search_term_mul in message_text
                if found:
                    return True
                return False

    # process filters
    datestamps = []
    filtered_messages = []
    if messages:
        if (start_date and end_date) or search_terms_cleaned:
            for message in messages:
                # date only
                if (start_date and end_date) and not search_terms_cleaned:
                    ret = valid_date(message)
                    if ret == 0:
                        continue
                    elif ret == -1:
                        break
                    else:
                        filtered_messages.append(message)

                # search only
                elif search_terms_cleaned and not (start_date and end_date):
                    ret = valid_search(message)
                    if ret:
                        filtered_messages.append(message)

                # both
                else:
                    ret = valid_date(message)
                    if ret == 0:
                        continue
                    elif ret == -1:
                        break
                    else:
                        if valid_search(message):
                            filtered_messages.append(message)

        else:
            filtered_messages = messages

        # process datestamps
        last = messages[0].date
        datestamps.append(1)
        for n, message in enumerate(filtered_messages):
            message_date = message.date
            if message_date.month != last.month or message_date.day != last.day or message_date.year != last.year:
                datestamps.append(n + 1)
                last = message.date

    context = {
        "handle": handle,
        "messages": filtered_messages,
        "datestamps": datestamps
    }

    return render(request, "messages/messages.html", context)

