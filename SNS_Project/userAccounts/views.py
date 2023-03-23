from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from friends.models import *
from .forms import *
from userPosts.forms import *
from userPosts.models import *

# function used to check if there are any friend requests
def have_request(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, pending=True)
    except FriendRequest.DoesNotExist:
        return False

# Create your views here.
def user_register(request):
    registered = False

    # if request method is POST, POST the data entered in the form
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        # if user_form data is valid, save it, and set the password to user.password
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # this is so that a 'profile' is also created for the user
            # UserAccount would have an instance for the user too (with empty fields)
            # UserAccount data can than be updated when the user edits their profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            # make registered status true
            registered=True

            # return success message
            messages.success(request, 'Account registered for ' + user.username)
            return redirect('user_login')
        else:
            messages.error(request, 'There was an error while processing your request')

    # else if the request method is GET, show the userform
    else:
        user_form = UserForm()

    # return data to be rendered
    return render(request, 'register.html', {'user_form': user_form, 
                                             'registered':registered})



def user_login(request):
    if request.method == 'POST':
        # post the username and password field, and authenticate them
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        # if login credentials is correct
        if user:
            # if the user account is_active
            if user.is_active:
                # log the user in and redirect to home page
                login(request, user)
                return redirect('/')

            # else return an error message
            else:
                messages.error(request, 'Your account has been suspended. Please contact administrator')
                return redirect('user_login')

        # else return error message for invalid login credentials
        else:
            messages.error(request, 'Invalid login details')
            return redirect('user_login')

    # return login page if request method is GET
    else:
        return render(request, 'login.html')



@login_required
def user_profile(request):
    context = {}
    user = request.user

    # if the user is authenticated and request method is GET
    if user.is_authenticated and request.method == 'GET':
        # get forms to display
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=user.profile)
        posts = UserPost.objects.filter(user=user)

        try:
            # get the friends of logged in user
            friend = Friend.objects.get(current_user=user)
        except Friend.DoesNotExist:
            friend_list = Friend(current_user=user)
            friend_list.save()
        
        # save friend list data of logged in user in context
        friend_list = friend.friends.all()
        context['friend_list'] = friend_list

        # filter UserAccount based on if user is in the friend_list
        # this is the get the profile image of friends
        profile = UserAccount.objects.filter(user__in=friend_list)
        context['profile'] = profile

        friend_requests = None

        try:
            # get all friend requests that are still pending
            friend_requests = FriendRequest.objects.filter(receiver = user, pending=True)

            images_list = []
            sender_list = []
            # find the User that matches the username from friend_requests, and append the image to images_list
            for username in friend_requests:
                sender = User.objects.get(username = username)
                profile_result = UserAccount.objects.get(user = sender)
                if profile_result.image:
                    profile_img = profile_result.image.url
                    images_list.append(profile_img)
                else:
                    images_list.append(None)

                if(have_request(sender = sender, receiver = user) != False):
                    sender_id = have_request(sender = sender, receiver = user).id
                    sender_list.append(sender_id)

            sender_info = zip(friend_requests, images_list, sender_list)
            context['sender_info'] = sender_info

        except:
            pass

        # save data in context
        context['friend_requests'] = friend_requests

        context['user'] = user
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        context['posts'] = posts
    else:
        messages.error(request, 'Please login first')
        return redirect('user_login')

    return render(request, 'profile.html', context)



@login_required
def user_editProfile(request):
    # if the user is authenticated
    if request.user.is_authenticated:
        # if request method is POST, POST the data in the UpdateUserForm and UpdateProfileForm
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
            
            # if the data in the 2 forms is valid, save them
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()

                # return success message
                messages.success(request, 'Your profile has been updated successfully')
                return redirect('user_editProfile')
            else:
                # else return success message
                messages.error(request, 'There is an error when updating your profile')
        # else if request method is GET, render the UpdateUserForm and UpdateProfileForm
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=request.user.profile)
    else:
        messages.error(request, 'Please login first')
        return redirect('user_login')

    return render(request, 'editProfile.html', {'user_form': user_form, 'profile_form': profile_form})



@login_required
def user_search(request):
    # if the user is authenticated
    if request.user.is_authenticated:
        # if request method is POST
        if request.method == "POST":
            # post the search
            search = request.POST['q']

            # if there is a user search request
            if search:
                # filter the search through the User model and get the result
                result=User.objects.filter(username__contains=search)
                
                # get the profile image of the result users
                images_list = []
                for user in result:
                    profile_result=UserAccount.objects.get(user=user)
                    if profile_result.image:
                        profile_img = profile_result.image.url
                        images_list.append(profile_img)
                    else:
                        images_list.append(None)
                search_result = zip(result, images_list)
            else:
                return render(request, 'search.html')
    else:
        messages.error(request, 'Please login first')
        return redirect('user_login')
    # return the search result to render
    return render(request, "search.html",{'search_result':search_result})



@login_required
def user_logout(request):
    # logout the user and return success message
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect("/")



@login_required
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
                messages.error(request, "An error has occurred when accepting friend request")
        else:
            messages.error(request, "Request does not exist")
    return HttpResponse



@login_required
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
                messages.error(request, "An error has occurred when declining friend request")
        else:
            messages.error(request, "Request does not exist")
    return HttpResponse