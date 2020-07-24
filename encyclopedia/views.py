from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown2
import random
from django.shortcuts import redirect

# Create your views here.

def index(request):
    return render(request, "encyclopedia/index.html", {"entries":util.list_entries()})

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

