from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *
from userAccounts.models import *
from userAccounts.forms import *
from userPosts.models import *

# function used to check if there are any friend requests
def have_request(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, pending=True)
    except FriendRequest.DoesNotExist:
        return False


# Create your views here.
def friendDetail(request, username):
    context = {}
    user = request.user
    
    if user.is_authenticated:
        if request.method == "GET":
            # get forms to display
            viewed_user = User.objects.get(username = username)
            profile = UserAccount.objects.get(user = viewed_user)
            profile_form = UserProfileForm(instance=user.profile)
            posts = UserPost.objects.filter(user=viewed_user)

            try:
                # get the friends of the viewed user
                friend = Friend.objects.get(current_user=viewed_user)
            except Friend.DoesNotExist:
                friend = Friend(current_user=viewed_user)
                friend.save()

            # save friend list data of viewed user in context
            friend_list = friend.friends.all()
            context['friend_list'] = friend_list

            # filter UserAccount based on if user is in the friend_list
            # this is the get the profile image of friends
            friend_profile = UserAccount.objects.filter(user__in=friend_list)
            context['friend_profile'] = friend_profile

            is_self = False
            is_friend = False
            # 0 - no request, 1 - request to user, 2 - request from user
            request_status = 0

            # check if user is friends with viewed user
            if friend_list.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                # if there is a friend request from viewed user to current user
                if have_request(sender = viewed_user, receiver = user) != False:
                    # set request_state to 1 [there is a request to user]
                    request_status = 1
                    # get the specific id from the friendRequest model, save in context
                    context['req_id'] = have_request(sender = viewed_user, receiver = user).id
                # if there is a friend request from current user to viewed user
                elif have_request(sender = user, receiver = viewed_user) != False:
                    # set request_state to 2 [there is a request from user]
                    request_status = 2
                else:
                    # set request_state to 0 [there is no user]
                    request_status = 0

            # save data in context
            context['is_self'] = is_self
            context['is_friend'] = is_friend
            context['request_status'] = request_status
            
            context['user'] = viewed_user
            context['profile'] = profile
            context['profile_form'] = profile_form
            context['posts'] = posts

    else:
        messages.error(request, 'Login first before viewing profile')
        return redirect('user_login')

    return render (request, 'friendDetail.html', context)



def sendRequest(request):
    currentUser = request.user

    if request.method == "POST" and currentUser.is_authenticated:
        # get user_id of reciever
        user_id = request.POST.get("receiverID")

        # if there user_id exists
        if user_id:
            # set reciever of the friend request to be the User with the user_id
            receiver = User.objects.get(pk=user_id)

            # check if there is any friend request from currentUser to receiver
            try:
                friend_requests = FriendRequest.objects.filter(sender=currentUser, receiver=receiver)

                try:
                    for req in friend_requests:
                        # if the request is still active (pending)
                        if req.pending:
                            messages.info(request, "There is a pending friend request to this user")
                    # send friend request
                    friend_request = FriendRequest(sender=currentUser, receiver=receiver)
                    friend_request.save()
                    messages.success(request, "Friend request successfully send")

                except Exception as e:
                    messages.error(request, "There is a error when sending friend request to this user")

            # if there is no friend request from current user to ANY user
            except FriendRequest.DoesNotExist:
                # send friend request
                friend_request = FriendRequest(sender=currentUser, receiver=receiver)
                friend_request.save()
                messages.success(request, "Friend request successfully send")

        # if no user_id
        else:
            messages.error(request, "User does not exist")
    return HttpResponse



def cancelRequest(request):
    currentUser = request.user

    if request.method == "POST" and currentUser.is_authenticated:
        # get user_id of reciever
        user_id = request.POST.get("receiverID")

        # if there user_id exists
        if user_id:
            # set reciever of the friend request to be the User with the user_id
            receiver = User.objects.get(pk=user_id)

            # check if there is any friend request from currentUser to receiver
            try:
                # get the request that is send
                reqToCancel = FriendRequest.objects.filter(sender=currentUser, receiver=receiver, pending=True)

                # there might be previous requests between the 2 users, so get the latest made request and cancel it
                reqToCancel.first().cancel()
                messages.success(request, "Friend request has been cancelled")
            
            except Exception as e:
                # return error msg
                messages.error(request, "An error has occurred, there is no friend request send to this user")

        # if no user_id
        else:
            messages.error(request, "User does not exist")
    return HttpResponse



def removeFriend(request):
    currentUser = request.user
    
    if request.method == "POST" and currentUser.is_authenticated:
        # get user_id of reciever
        user_id = request.POST.get("receiverID")

        # if there user_id exists
        if user_id:
            try:
                # get the FriendToRemove (using the user_id) from the User model
                FriendToRemove = User.objects.get(pk=user_id)

                # get the FriendToRemove from Friend model, and call the unfriend method 
                # to remove the friend from authenticated user's own friend list
                self_friend_list = Friend.objects.get(current_user=currentUser)
                self_friend_list.unfriend(FriendToRemove)
                
                messages.success(request, FriendToRemove.username + " has been removed from friend list")

            except Exception as e:
                # return error msg
                messages.error(request, "An error has occurred")
        else:
            messages.error(request, "Friend does not exist")
    return HttpResponse



def acceptRequest(request, *args, **kwargs):
    currentUser = request.user

    if request.method == "GET" and currentUser.is_authenticated:

        # get id of request
        req_id = kwargs.get("req_id")

        # if the req_id exists
        if req_id:
            # get the req object based on the req_id
            friend_request = FriendRequest.objects.get(pk=req_id)

            try:
                # call accept method on the friend_request
                friend_request.accept()
                messages.success(request, "Friend request has been accepted")

            except Exception as e:
                # return error msg
                messages.error(request, "An error has occurred when accepting friend request")
        else:
            messages.error(request, "Request does not exist")
    return HttpResponse



def declineRequest(request, *args, **kwargs):
    currentUser = request.user
    
    if request.method == "GET" and currentUser.is_authenticated:

        # get id of request
        req_id = kwargs.get("req_id")

        # if the req_id exists
        if req_id:
            # get the req object based on the req_id
            friend_request = FriendRequest.objects.get(pk=req_id)

            try:
                # call decline method on the friend_request
                friend_request.decline()
                messages.success(request, "Friend request has been declined")
            except Exception as e:
                # return error msg
                messages.error(request, "An error has occurred when declining friend request")
            
        else:
            messages.error(request, "Request does not exist")
    return HttpResponse