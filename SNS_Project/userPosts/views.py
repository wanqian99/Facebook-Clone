import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
from .forms import *
from userAccounts.models import *
from userAccounts.forms import *
from friends.models import *

# Create your views here.
def home(request, *args, **kwargs):
    context = {}
    currentUser = request.user

    # check if request method is post and that the user is authenticated
    if request.method == "POST" and currentUser.is_authenticated:
        # get the user post form
        post_form = UserPostForm(request.POST, request.FILES)

        # check if the post_form is valid
        if post_form.is_valid():
            # get the cleaned_data
            content = post_form.cleaned_data.get("content")
            try: 
                # request for file upload where the input name is 'postImage'
                request_file = request.FILES['postImage']
                # location of media folder 
                url = os.path.join(settings.MEDIA_ROOT)
                fss = FileSystemStorage(location=url)
                # stores image at media/postImage directory
                file = fss.save(f"postImage/{str(request_file)}", request_file)

                # create a UserPost object with the content, file, currentUser information
                new_post = UserPost.objects.create(content=content, content_image=file, user=currentUser)

                # return success message
                messages.success(request, 'Successfully uploaded a new post')
                return HttpResponseRedirect("/")
            except:
                # if there is no image uploaded by the user, create the UserPost with only the content and currenUser
                new_post = UserPost.objects.create(content=content, user=currentUser)

                # return success message
                messages.success(request, 'Successfully uploaded a new post')
                return HttpResponseRedirect("/")

    # if the user is authenticated
    if currentUser.is_authenticated:
        # get the profile form from userAccounts app whereby the data is the currentUser's profile
        profile_form = UpdateProfileForm(instance=currentUser.profile)
        context['profile_form'] = profile_form

        friend_list = []
        try:
            # get the friends of the currentUser
            currentUser_friend_list = Friend.objects.get(current_user=currentUser)
            # append each friend object to the friend_list
            for friend in currentUser_friend_list.friends.all():
                friend_list.append(friend)
        except Friend.DoesNotExist:
            pass

        # if there are friend in the friend_list, display currentUser's post and their friends' posts
        if friend_list != []:
            # include currentUser to list before filtering
            friend_list.append(currentUser)

            # filter UserPost based on if user is in the friend_list
            # order by timestamp and reverse filtered result so that posts are correctly displayed on the home page
            # (new post displayed before old post)
            posts = reversed(UserPost.objects.filter(user__in=friend_list).order_by('timestamp'))
            context['posts'] = posts

            # filter UserAccount based on if user is in the friend_list
            # this is to get the profile image of friends
            profile = UserAccount.objects.filter(user__in=friend_list)
            context['profile'] = profile
            
        # else if friend_list is empty
        else:
            # display own posts only
            # order by timestamp and reverse filtered result so that posts are correctly displayed on the home page
            # (new post displayed before old post)
            posts = reversed(UserPost.objects.filter(user=currentUser).order_by('timestamp'))
            context['posts'] = posts

            # filter UserAccount based on if user is in the friend_list
            # this is to get the profile image of friends
            profile = UserAccount.objects.get(user=currentUser)
            context['profile'] = profile

        # for the navbar in header.html to display the active state of the home icon correctly
        context['navbar'] = "home"
    return render(request, "home.html", context)