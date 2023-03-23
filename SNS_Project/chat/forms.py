from django import forms
from .models import *

class ChatroomForm(forms.ModelForm):
    chatroom = forms.CharField(required=True, 
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder':'Enter chatroom name...',
                                                             'label': 'Create a new chatroom'}))
    # user = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Chatroom
        fields = ['chatroom']