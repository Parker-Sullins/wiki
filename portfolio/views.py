from django.shortcuts import render
from .models import Project
from encyclopedia import util
from markdown2 import markdown, markdown_path

hey = markdown_path('media/entries/Git.md')





def home(request):
    mdm = []
    ent = util.list_entries()
    for entry in ent:
        mdm.append(util.get_entry(entry))
    projects = Project.objects.all()
    return render(request, "portfolio/home.html", {'projects': projects, 'entries': mdm, 'try': hey})
