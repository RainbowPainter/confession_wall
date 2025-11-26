from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Confession, Comment


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="邮箱")

    class Meta:


        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ConfessionForm(forms.ModelForm):
    class Meta:
        model = Confession
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '写下你的表白内容...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'content': '表白内容',
            'image': '上传图片（可选）'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '写下你的评论...'
            })
        }
        labels = {
            'content': '评论'
        }