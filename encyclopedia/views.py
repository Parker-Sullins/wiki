from django.shortcuts import render
from . import util


def index(request):
    return render(request, "encyclopedia/home.html", {
        "entries": util.list_entries()
    })

def create_page(request):
    return render(request, "encyclopedia/create_page.html")

def entry(request):
    return render(request, "encyclopedia/entry.html")
