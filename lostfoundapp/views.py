from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Item, Profile
from .forms import ItemForm, ProfileForm
from django.db.models import Q

@login_required
def home(request):
    items = Item.objects.all().order_by('-posted_at')
    return render(request, 'home.html', {'items': items})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def post_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.posted_by = request.user
            item.save()
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'post_item.html', {'form': form})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item_detail.html', {'item': item})

def search(request):
    query = request.GET.get('q', '')
    item_type = request.GET.get('type', '')
    items = Item.objects.all().order_by('-posted_at')
    
    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(location__icontains=query)
        )
        
    if item_type in ['lost', 'found']:
        items = items.filter(item_type=item_type)
        
    return render(request, 'search.html', {'items': items, 'query': query, 'item_type': item_type})

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST' and item.posted_by == request.user:
        item.delete()
        return redirect('home')
    return redirect('item_detail', pk=pk)

@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})
