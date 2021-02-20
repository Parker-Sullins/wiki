from django.shortcuts import render
from . import util
from markdown2 import markdown, markdown_path

def index(request):
    return render(request, "encyclopedia/home.html", {
        "entries": util.list_entries()
    })

def create_page(request):
    return render(request, "encyclopedia/create_page.html")


def entry(request):
    name = util.list_entries()
    name = str(name[4])
    hey = markdown_path('media/entries/' + name + '.md')
    return render(request, "encyclopedia/entry.html", {'entry': hey})
