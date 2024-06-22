from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from random import shuffle
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User 
from django.contrib import messages
from .models import Photo, Comment
from .forms import PhotoForm, CommentForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'base/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home') 
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'base/login.html', {'form': form})

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('home')
    else:
        form = PhotoForm()
    return render(request, 'base/upload_photo.html', {'form': form})

def home(request):
    photos = Photo.objects.all()
    shuffled_photos = list(photos)
    shuffle(shuffled_photos)

    context = {
        'photos': shuffled_photos,
    }
    return render(request, 'base/home.html', context)


@login_required
def add_comment(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.photo = photo
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'base/add_comment.html', {'form': form})

@login_required
def edit_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id, user=request.user)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PhotoForm(instance=photo)
    return render(request, 'base/edit_photo.html', {'form': form})

@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id, user=request.user)
    if request.method == 'POST':
        photo.delete()
        return redirect('home')
    return render(request, 'base/delete_photo.html', {'photo': photo})


@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    user_photos = Photo.objects.filter(user=user_profile)
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, 'Photo uploaded successfully.')
            return redirect('profile', username=request.user.username)
    else:
        form = PhotoForm()

    return render(request, 'base/profile.html', {
        'profile': user_profile,
        'form': form,
        'user_photos': user_photos,
    })