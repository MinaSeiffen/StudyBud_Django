from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {'id':1, 'name':"mina emad", },
#     {'id':2, 'name':"mina emad lets learn something new", },
#     {'id':3, 'name':"mina emad hey", },
#     {'id':4, 'name':"mina emad lolz", },
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist!')
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist!')
    context = {'page': page}
    return render(request, 'base/login_registration_page.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registrationPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error happened while registration')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_registration_page.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q(name__icontains = q) | Q(description__icontains = q))
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    context = {'rooms':rooms, 'topics': topics, 'rooms_count': rooms_count}
    return render(request,'base/home.html' , context)

def room(request,pk):
    # room = None
    # rooms = Room.objects.all()
    # for i in rooms:
    #     if i.id == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request,'base/room.html',context)

@login_required(login_url = 'login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        # request.POST.get('name')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def update_room(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You do not have the permission to do that')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def delete_room(request, pk):
    room = Room.objects.get(id=int(pk))

    if request.user != room.host:
            return HttpResponse('You do not have the permission to do that')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj' : room.name}
    return render(request, 'base/delete.html' ,context )