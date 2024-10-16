from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, 'User does not exist!')
        user = authenticate(request, email = email, password = password)

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
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
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
    topics = Topic.objects.all()[0:5]
    rooms_count = rooms.count()
    room_messages = Message.objects.all().filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics': topics, 'rooms_count': rooms_count, 'room_messages': room_messages}
    return render(request,'base/home.html' , context)

def room(request,pk):
    # room = None
    # rooms = Room.objects.all()
    # for i in rooms:
    #     if i.id == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room, 'room_messages': room_messages, 'participants': participants}
    return render(request,'base/room.html',context)

def get_profile(request, pk):
    user = User.objects.get(id = int(pk))
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, "room_messages": room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url = 'login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name= topic_name)
        Room.objects.create(
            host= request.user,
            topic= topic,
            name= request.POST.get('name'),
            description= request.POST.get('description'),
        )
        return redirect('home')
        # request.POST.get('name')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def update_room(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You do not have the permission to do that')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name= topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('home')

    context = {'form': form, "topics": topics, "room": room}
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

@login_required(login_url = 'login')
def delete_message(request, pk):
    message = Message.objects.get(id=int(pk))

    if request.user != message.user:
            return HttpResponse('You do not have the permission to do that')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj' : message}
    return render(request, 'base/delete.html' ,context )

@login_required(login_url= 'login')
def update_user(request):
    user = request.user
    form = UserForm(instance= user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance= user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk= user.id)

    context = {'form': form}
    return render(request, 'base/edit-user.html', context)

def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains= q)

    context = {'topics': topics}
    return render(request, 'base/topics.html', context)

def activity_page(request):
    room_messages = Message.objects.all()[0:3]

    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)