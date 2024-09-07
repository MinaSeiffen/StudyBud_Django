from django.shortcuts import render
from .models import Room

# rooms = [
#     {'id':1, 'name':"mina emad", },
#     {'id':2, 'name':"mina emad lets learn something new", },
#     {'id':3, 'name':"mina emad hey", },
#     {'id':4, 'name':"mina emad lolz", },
# ]

def home(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
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