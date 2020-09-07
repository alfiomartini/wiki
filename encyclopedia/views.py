from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import myutil
import markdown2, random
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# see: https://stackoverflow.com/questions/3578882/how-to-specify-the-login-required-redirect-url-in-django
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User

# Create your views here.

def index(request):
    if  not request.user.is_authenticated:
        return render(request, 'encyclopedia/login.html', {'message':None})
    else:
        return render(request, "encyclopedia/index.html", {"entries":myutil.list_entries()})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user)
            request.session['name_id'] = username
            return redirect('index')
        else:
            return render(request, 'encyclopedia/login.html', {'message':"Invalid credentials!"})
    else:
        return render(request, 'encyclopedia/login.html', {'message':None})        

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "encyclopedia/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        # https://stackoverflow.com/questions/29588808/django-how-to-check-if-username-already-exists
        if User.objects.filter(username=username).exists():
            return render(request, "encyclopedia/register.html", {
                "message": "Username already taken."})
        else:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            return redirect('index')    
    else:
        return render(request, "encyclopedia/register.html")

@login_required(login_url='index')
def logout_view(request):
    logout(request)
    request.session.clear()
    return render(request, 'encyclopedia/login.html', {'message': 'Logged out'})

@login_required(login_url='index')
def random_page(request):
    entries = myutil.list_entries()
    size = len(entries)
    index = random.randint(0, size - 1)
    entry_id = entries[index]
    return redirect(f'/wiki/{entry_id}')

@login_required(login_url='index')
def entry(request, entry_id):
    entry = myutil.get_entry(entry_id)
    if entry:
        entry = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {'title':entry_id, 'content':entry})
    else:
        return render(request, "encyclopedia/error.html", {"message":f"Entry {entry_id} not found!"})

@login_required(login_url='index')
def newpage(request):
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        entries = myutil.list_entries()
        if title in entries:
            return render(request, 'encyclopedia/error.html', {'message':f"Entry {title} already exists!"})
        else:
            myutil.save_entry(title, text)
            return redirect(f'/wiki/{title}')
    else:
        return render(request, 'encyclopedia/newpage.html')

@login_required(login_url='index')
def edit(request, entry_id):
    entry = myutil.get_entry(entry_id)
    return render(request, 'encyclopedia/editpage.html', {'title':entry_id, 'text':entry})

@login_required(login_url='index')
def savedit(request):
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        myutil.save_entry(title, text)
        return redirect(f'/wiki/{title}')

@login_required(login_url='index')
def search(request, term):
    new_list = []
    entries = myutil.list_entries()
    for k in range(len(entries)):
        entries[k] = entries[k].lower()
    if term.lower() in entries:
        return redirect(f'/wiki/{term}')
    for entry in entries:
        if term.lower() in entry:
            new_list.append(entry.capitalize())
    return render(request, "encyclopedia/search.html", {"entries":new_list})
    



