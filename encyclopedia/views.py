from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import util
import markdown2
import random
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    if  not request.user.is_authenticated:
        return render(request, 'encyclopedia/login.html', {'message':None})
    else:
        return render(request, "encyclopedia/index.html", {"entries":util.list_entries()})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'encyclopedia/login.html', {'message':"Invalid credentials!"})

def logout_view(request):
    logout(request)
    return render(request, 'encyclopedia/login.html', {'message': 'Logged out'})

def random_page(request):
    entries = util.list_entries()
    size = len(entries)
    index = random.randint(0, size - 1)
    entry_id = entries[index]
    return redirect(f'/wiki/{entry_id}')

def entry(request, entry_id):
    entry = util.get_entry(entry_id)
    if entry:
        entry = markdown2.markdown(entry)
        # return HttpResponse(entry)
        return render(request, "encyclopedia/entry.html", {'title':entry_id, 'content':entry})
    else:
        return render(request, "encyclopedia/error.html", {"message":f"Entry {entry_id} not found!"})

def newpage(request):
    if request.method == 'POST':
        title = request.POST['title']
        # print(title)
        text = request.POST['text']
        # print(text)
        entries = util.list_entries()
        if title in entries:
            return render(request, 'encyclopedia/error.html', {'message':f"Entry {title} already exists!"})
        else:
            util.save_entry(title, text)
            return redirect(f'/wiki/{title}')
    else:
        return render(request, 'encyclopedia/newpage.html')
      
def edit(request, entry_id):
    entry = util.get_entry(entry_id)
    # entry = markdown2.markdown(entry)
    # print(entry)
    return render(request, 'encyclopedia/editpage.html', {'title':entry_id, 'text':entry})

def savedit(request):
    if request.method == 'POST':
        title = request.POST['title']
        # print(title)
        text = request.POST['text']
        # print(text)
        util.save_entry(title, text)
        return redirect(f'/wiki/{title}')

def search(request, term):
    # print(term)
    new_list = []
    entries = util.list_entries()
    for k in range(len(entries)):
        entries[k] = entries[k].lower()
    # print(entries)
    if term.lower() in entries:
        return redirect(f'/wiki/{term}')
    for entry in entries:
        if term.lower() in entry:
            new_list.append(entry)
    return render(request, "encyclopedia/search.html", {"entries":new_list, "term":term})
    



