from crypt import methods
from django.contrib import messages
from django.shortcuts import render, redirect

from chat.forms import ChatroomForm
from .models import *
from .forms import *
from userAccounts.models import *
from userAccounts.forms import *

# Create your views here.
def chat(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            chatroomForm = ChatroomForm(request.POST)
            if chatroomForm.is_valid():
                chatroomForm.save()
                chatroom = request.POST['chatroom']
                messages.success(request, 'Chatroom created successfully')
                return redirect('/chat/' + chatroom)
            else:
                messages.error(request, 'There was an error when creating the chatroom')
                return redirect('chat')
        else:
            profile_form = UpdateProfileForm(instance=request.user.profile)
            chatroom = Chatroom.objects.all()

            # show create chatroom form
            chatroomForm = ChatroomForm()

            # save data to chatroom
            context['profile_form'] = profile_form
            context['navbar'] = "chat"
            context['chatroom'] = chatroom
            context['chatroomForm'] = chatroomForm
        return render(request, 'chat.html', context)
    else:
        messages.error(request, 'Please login first')
        return redirect('user_login')



def room(request, chatroom_name):
    context = {}
    if request.user.is_authenticated:
        if request.method == "GET":
            profile_form = UpdateProfileForm(instance=request.user.profile)
            context['profile_form'] = profile_form
            context['navbar'] = "chat"
            context['chatroom_name'] = chatroom_name
        # else:
        #     message = request.POST.get('chat-message-input')
        #     room = Chatroom.objects.get(chatroom = chatroom_name)

        #     new_message = ChatroomContent.objects.create(content=message, user=request.user, chatroom=room)
        #     new_message.save()
        #     return redirect('/chat/' + chatroom_name)

        return render(request, 'room.html', context)
    else:
        messages.error(request, 'Please login first')
        return redirect('user_login')



def deleteChatroom(request, chatroom_name):
    # if user wants to delete the chatroom
    try:
        chatroom = Chatroom.objects.get(chatroom = chatroom_name)
        chatroom.delete()
        messages.success(request, 'Chatroom deleted successfully')
        return redirect('chat')
    except:
        messages.error(request, 'There was an error when deleting the chatroom')
        return redirect('chat')