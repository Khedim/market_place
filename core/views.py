from django.shortcuts import render, redirect
from items.models import Item, Category
from .forms import SinupForm


def index(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()[:6]
    context = {
        'items': items, 
        'categories': categories
    }
    return render(request, 'core/index.html', context)


def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SinupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else :
        form = SinupForm()
    context = {
        'form': form
    }
    return render(request, 'core/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = SinupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else :
        form = SinupForm()
    context = {
        'form': form
    }
    return render(request, 'core/signup.html', context)