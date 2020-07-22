from django.shortcuts import render
from . import util

# Create your views here.

def index(request):
  return render(request, "encyclopedia/index.html", {"entries":util.list_entries()})
