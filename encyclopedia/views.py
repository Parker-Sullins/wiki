from django.shortcuts import render
from . import util
from markdown2 import markdown, markdown_path
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Enter Title")
    description = forms.CharField(label="Enter Description")


class EditForm(forms.Form):
    description = forms.CharField(label="Edit Description")


def index(request):
    request.session["entries"] = util.list_entries()
    return render(request, "encyclopedia/home.html", {
        "entries": request.session["entries"]
    })


def entry(request, title):
    title = title
    entry = markdown_path('media/entries/' + title + '.md', extras=["break-on-newline"])
    return render(request, "encyclopedia/entry.html", {
        'entry': entry,
        'title': title
    })


def contribute(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            title = form.cleaned_data["title"]
            description_formatted = '#' + title.title() + '\n' + description.capitalize()
            request.session['new_entry'] = util.save_entry(title, description_formatted)
            request.session["entries"].append(request.session['new_entry'])
            return HttpResponseRedirect(reverse("encyclopedia:home"))
        else:
            return render(request, "encyclopedia/contribute.html", {
                "form": form
            })
    return render(request, "encyclopedia/contribute.html", {
            'form': NewEntryForm()
            })


def edit(request, title):
    form = EditForm()
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            title_2 = title
            description_formatted = '#' + title_2.title() + '\n' + description.capitalize()
            util.save_entry(title_2, description_formatted)
            return HttpResponseRedirect(reverse("encyclopedia:home"))
        else:
            return render(request, "encyclopedia/contribute.html", {"form": form})
    return render(request, "encyclopedia/edit.html", {
        'title': title,
        'form': form
    })
