from django.db import models
from userAccounts.models import *

# Create your models here.

# User Account model extended from Django User model
class Friend(models.Model):
    current_user = models.OneToOneField(User,related_name='current_user', on_delete=models.CASCADE, null=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    def __str__(self):
        return self.current_user.username

    def add_friend(self, to_be_added):
        # if to_be_added is not in friend list, add account as friend
        if not to_be_added in self.friends.all():
            self.friends.add(to_be_added)
            self.save()

    def remove_friend(self, to_be_removed):
        # if to_be_removed is in friend list, remove account as friend
        if to_be_removed in self.friends.all():
            self.friends.remove(to_be_removed)
            self.save()

    def unfriend(self, user_to_remove):
        # remove account from user's friend list
        self.remove_friend(user_to_remove)

        # remove user from friend's friend list
        friends_list = Friend.objects.get(current_user=user_to_remove)
        friends_list.remove_friend(self.current_user)


    
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'sender')
    receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'receiver')
    pending = models.BooleanField(blank = True, null = False, default = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.sender.username

    # add sender to reciever's friend list, add reciever to sender's friend list,
    def accept(self):
        # get the user that recieved the friend request
        recieved_req = Friend.objects.get(current_user=self.receiver)

        # if recieved friend request
        if recieved_req:
            # call add_friend function sender [sender adds receiver]
            recieved_req.add_friend(self.sender)

            # get the user that send the friend request
            send_req = Friend.objects.get(current_user=self.sender)
            
            # call add_friend function on receiver [receiver adds sender]
            send_req.add_friend(self.receiver)

            # set pending to false and save
            self.pending = False
            self.save()
    
    # set the pending state for the friend request to False
    def decline(self):
        # make pending false when user declined friend request
        self.pending = False
        self.save()

    # cancel sent friend request
    def cancel(self):
        # make request_state false when user cancel friend request
        self.pending = False
        self.save()