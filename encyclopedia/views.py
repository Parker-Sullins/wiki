from django.shortcuts import render
from . import util
from markdown2 import markdown_path
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Enter Title")
    description = forms.CharField(label="Enter Description", widget=forms.Textarea)


class EditForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)


def index(request):
    rand_list = random.choice(util.list_entries())
    request.session["entries"] = util.list_entries()
    return render(request, "encyclopedia/home.html", {
        "entries": request.session["entries"],
        "random": rand_list
    })


def entry(request, title):
    rand_list = random.choice(util.list_entries())
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", {'title': title, 'random': rand_list})
    entry_formatted = markdown_path('media/entries/' + title + '.md', extras=["break-on-newline"])
    return render(request, "encyclopedia/entry.html", {
        'entry': entry_formatted,
        'title': title,
        "random": rand_list
    })


def contribute(request):
    rand_list = random.choice(util.list_entries())
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            check_for_entry = util.list_entries()
            f = form.cleaned_data["title"]
            check = f.lower()
            check_list = [x.lower() for x in check_for_entry]
            for i in check_list:
                if check == i:
                    error = "Entry Already Exist!"
                    return render(request, "encyclopedia/contribute.html", {"form": form,
                                                                            "error": error,
                                                                            "random": rand_list})
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
            'form': NewEntryForm(),
            "random": rand_list
            })


def edit(request, title):
    rand_list = random.choice(util.list_entries())
    pre_populate = util.get_entry(title)
    pre_populate = pre_populate.replace(("#" + title), "", 1)
    f = EditForm(initial={'description': pre_populate})
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            title_2 = title
            description_formatted = '#' + title_2.title() + '\n' + description.capitalize()
            util.save_entry(title_2, description_formatted)
            return HttpResponseRedirect("/wiki/" + title_2)
        else:
            return render(request, "encyclopedia/contribute.html", {"form": form})
    return render(request, "encyclopedia/edit.html", {
        'title': title,
        'form': f,
        'random': rand_list
    })


def error(request, catch):
    rand_list = random.choice(util.list_entries())
    return render(request, "encyclopedia/error.html", {
        "catch": catch,
        "random": rand_list
    })


def search_results(request):
    rand_list = random.choice(util.list_entries())
    if request.method == 'POST':
        all_entries = util.list_entries()
        converted_entries = [x.lower() for x in all_entries]
        query_entries = []
        search_query = request.POST.get("q").lower()
        for x in all_entries:
            if search_query == x.lower():
                return HttpResponseRedirect("/wiki/" + search_query + "/")
        for entry in converted_entries:
            if search_query in entry:
                query_entries.append(entry)
        titles = [x.capitalize() for x in query_entries]
        return render(request, "encyclopedia/search_results.html", {
            'entries': titles,
            'query': search_query.capitalize(),
            "random": rand_list
        })

#            if search_query == entry:
#                return HttpResponseRedirect("/wiki/" + entry)
