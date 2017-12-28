from django.shortcuts import render
from django.conf import settings
from os.path import join
from os import listdir


def index(request):
    return render(request, 'home.html', {})


def databases(request):
    changed = False
    files = listdir(join(join(settings.PROJECT_ROOT, 'db')))
    dbs = []
    for file in files:
        if file.endswith(".db"):
            dbs.append(file)
    selected_db = settings.DATABASE_NAME
    config_db = open(join(join(settings.PROJECT_ROOT, 'db'), "db.conf"), "r").read().strip()

    if "select" in request.GET and request.GET["select"]:
        select = request.GET["select"].strip()
        if select != config_db:
            with open(join(join(settings.PROJECT_ROOT, 'db'), "db.conf"), "w") as f:
                f.write(select)

            # Jank way of implementing the syncdb functionality below. Works because django hot reloads.
            # from django.core.management import execute_from_command_line
            # execute_from_command_line("syncdb")
            with open(join(settings.CORE_APP_ROOT, "__init__.py"), "w") as f:
                f.write("#" + select)

            selected_db = select
            config_db = select
            changed = True

    context = {
        "databases": dbs,
        "selected": selected_db,
        "config_db": config_db,
        "changed": changed
    }
    return render(request, 'db.html', context)
