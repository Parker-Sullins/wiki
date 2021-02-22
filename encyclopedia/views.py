from django.shortcuts import render
from . import util
from markdown2 import markdown_path
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random


class NewEntryForm(forms.Form):
    """
    Form For Adding New entries. Takes a title and description field.
    """
    title = forms.CharField(label="Enter Title")
    description = forms.CharField(label="Enter Description", widget=forms.Textarea)


class EditForm(forms.Form):
    """
    Form for editing entries. Only Descriptions are editable.
    """
    description = forms.CharField(widget=forms.Textarea)


"""
 rand_list = random.choice(util.list_entries())
 
Stores a random entry to redirect the user to if the 
random button is clicked. Had to be accessible from 
every instance of,  render(request, URL), as template URL tags 
were not able to take arguments as I was expecting.
Refactoring needed.
"""


def index(request):
    rand_list = random.choice(util.list_entries())
    """
    View function For landing page. Links to home.html.
    Displays all current entries.
    """
    request.session["entries"] = util.list_entries()
    return render(request, "encyclopedia/home.html", {
        "entries": request.session["entries"],
        "random": rand_list
    })


def entry(request, title):
    rand_list = random.choice(util.list_entries())
    """
    If a url for an entry DNE, returns an error page.
    Else, it returns the entry populated with the markdown title and
    description.
    """
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
    """
    If method == POST, checks if entry already exist & displays warning, 
    if not, it adds entry to /entries/ and redirects to the home page
    """
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            form_title = form.cleaned_data["title"].lower()
            check_list = util.list_entries()
            check_list_low = [x.lower() for x in check_list]
            for title in check_list_low:
                if form_title == title:
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
    """
    If method == GET, returns a blank form to add a new entry.
    """
    return render(request, "encyclopedia/contribute.html", {
            'form': NewEntryForm(),
            "random": rand_list
            })


def edit(request, title):
    rand_list = random.choice(util.list_entries())
    """
    If method == Post, it updates the entries' description
    """
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
    """
    If method == Get, it populates the form with
    the existing description for each entry
     """
    pre_populate = util.get_entry(title)
    pre_populate = pre_populate.replace(("#" + title), "", 1)
    f = EditForm(initial={'description': pre_populate})

    return render(request, "encyclopedia/edit.html", {
        'title': title,
        'form': f,
        'random': rand_list
    })


def error(request, catch):
    """
    Displays error page. Will catch entries that DNE if they are accessed
    from the url directly.
    """
    rand_list = random.choice(util.list_entries())
    return render(request, "encyclopedia/error.html", {
        "catch": catch,
        "random": rand_list
    })


def search_results(request):
    """
    Takes input from user, and runs a search through all
    existing entries to identify if the search is a sub-string
    of any entries. Will return all entries in which the input
    is a sub string. If the Input is an exact match for an entry, it redirects straight
    to the url for that entry. If the input is a sub string of no entries
    it returns a DNE warning.
    """
    rand_list = random.choice(util.list_entries())
    if request.method == 'POST':
        all_entries = util.list_entries()
        converted_entries = [x.lower() for x in all_entries]
        query_entries = []
        search_query = request.POST.get("q").lower()
        for x in all_entries:
            if search_query == x.lower():
                return HttpResponseRedirect("/wiki/" + search_query.capitalize() + "/")
        for entry in converted_entries:
            if search_query in entry:
                query_entries.append(entry)
        titles = [x.capitalize() for x in query_entries]
        return render(request, "encyclopedia/search_results.html", {
            'entries': titles,
            'query': search_query.capitalize(),
            "random": rand_list
        })
