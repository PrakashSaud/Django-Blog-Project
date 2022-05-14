from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blog, Comment


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea, required=True)
    sender = forms.EmailField(required=True)


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('title', 'author', 'content')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('commented_by', 'comment_desc')


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user