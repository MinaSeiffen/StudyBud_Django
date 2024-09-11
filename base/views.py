from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {'id':1, 'name':"mina emad", },
#     {'id':2, 'name':"mina emad lets learn something new", },
#     {'id':3, 'name':"mina emad hey", },
#     {'id':4, 'name':"mina emad lolz", },
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics}
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

def update_room(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def delete_room(request, pk):
    room = Room.objects.get(id=int(pk))
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj' : room.name}
    return render(request, 'base/delete.html' ,context )