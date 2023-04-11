from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Item, Category
from .forms import AddItemForm, EditItemForm

# Create your views here.
def items(request):
    query = request.GET.get('query', '')
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()
    category_id = request.GET.get('category', 0)

    if query:
        items = Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_id:
        items = Item.objects.filter(category_id=category_id)

    context = {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    }
    return render(request, 'item/items.html', context)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]
    context = {
        'item': item,
        'related_items': related_items
    }
    return render(request, 'item/detial.html', context)

@login_required
def addItem(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = AddItemForm()
    context = {
        'form': form,
        'title': 'New Item'
    }
    return render(request, 'item/form.html', context)

@login_required
def editItem(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    context = {
        'form': form,
        'title': 'Edit Item'
    }
    return render(request, 'item/form.html', context)

def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')
