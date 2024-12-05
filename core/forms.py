
from .models import Member , Posts
from django import forms
from django.forms import ModelForm


class MemberForm(ModelForm):
    username = forms.CharField(max_length=30)

    class Meta:
        model = Member
        fields = ['batch', 'faculty', 'profile_pic', 'username']
        exclude = ['user']
class CreatePostForm(ModelForm):
    class Meta:
        model = Posts
        fields = '__all__'
        exclude =['date_created','member']