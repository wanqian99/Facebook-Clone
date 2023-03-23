from django import forms
from .models import *

class UserPostForm(forms.ModelForm):
    content = forms.CharField(required=True, 
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder':'Write something...',
                                                           'style': 'min-width: 100%',
                                                           'row': '10'}))
    content_image = forms.ImageField(label="image", required=False,
                                     widget=forms.FileInput(attrs={'class': 'form-control-file',
                                                                  'id': 'postImage',
                                                                  'oninput': 'addImage(this)'}))
    # user = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = UserPost
        fields = ['content', 'content_image']