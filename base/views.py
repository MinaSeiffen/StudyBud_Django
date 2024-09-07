from django.shortcuts import render
from django.http import HttpResponse

rooms = [
    {'id':1, 'name':"mina emad", },
    {'id':2, 'name':"mina emad lets learn something new", },
    {'id':3, 'name':"mina emad hey", },
    {'id':4, 'name':"mina emad lolz", },
]
def home(request):
    context = {'rooms':rooms}
    return render(request,'base/home.html' , context)

def room(request,pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room':room}
    return render(request,'base/room.html',context)