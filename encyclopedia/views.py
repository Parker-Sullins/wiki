from django.shortcuts import render
from . import util


def index(request):
    return render(request, "encyclopedia/home.html", {
        "entries": util.list_entries()
    })

def create_page(request):
    return render(request, "encyclopedia/create_page.html")
#../../../encyclopedia/static/encyclopedia/styles.css
#<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">