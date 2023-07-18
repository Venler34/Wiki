from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.defaultfilters import linebreaksbr
from markdown2 import Markdown
from django import forms
import random

from . import util

class SearchForm(forms.Form):
    searchItem = forms.CharField(label='',widget = forms.TextInput(attrs={'placeholder' : 'Search Encyclopedia'}))


def index(request):
    listOfEntries = util.list_entries()

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data["searchItem"]

            if util.get_entry(value) == None:
                results = []
                for entry in listOfEntries:
                    if value in entry:
                        results.append(entry)
                
                return render(request, "encyclopedia/searchResults.html", {
                    "entries" : results,
                    "form" : SearchForm()
                })

            return redirect('getEntry', title=value)
        
    return render(request, "encyclopedia/index.html", {
        "entries": listOfEntries,
        "form" : SearchForm()
    })


# Add error if entry does not exist
def getEntry(request, title):
    entry = util.get_entry(title)
    result = None

    if entry == None:
        heading = "<h1>Error</h1>"
        errorMessage = f"<p>Sorry, but we couldn't find the page called '{title}'.</p>"
        result = heading + "<br>" + errorMessage
        title = "Error"
    else:
        converter = Markdown()
        result = converter.convert(entry)

    return render(request, "encyclopedia/entry.html", {
        "title" : title,
        "result" : result,
        "form" : SearchForm()
    })

def newPage(request):
    if request.method == "POST":
        #dictionary
        data = request.POST
        title = data["title"]
        content = data["content"]
        
        if util.get_entry(title) != None:
            return render(request, "encyclopedia/newPage.html",{
                "Error" : True
            })
        else:
            util.save_entry(title, content)
            return redirect('getEntry', title=title)
        
    return render(request, "encyclopedia/newPage.html", {
        "Error" : False
    })

def editPage(request, title):

    if request.method == "POST":
        data = request.POST

        content = data["content"]

        util.save_entry(title, content)
        return redirect('getEntry', title=title)

    content = util.get_entry(title)

    return render(request, "encyclopedia/editPage.html", {
        "content" : content,
        "title" : title
    })

def randomPage(request):
    listOfEntries = util.list_entries()

    n = len(listOfEntries)

    index = random.randint(0,n-1)

    return redirect('getEntry', title=listOfEntries[index])