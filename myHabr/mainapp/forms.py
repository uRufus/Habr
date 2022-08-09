from django import forms

from .models import BlogPost, Comment


class BlogPostForm(forms.ModelForm):
    """Данная форма работает только с подключенным бутстрапом"""

    class Meta:
        model = BlogPost
        fields = ('title', 'blog', 'body')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'blog': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),

        }


class CommentForm(forms.ModelForm):
    # comment = forms.CharField(
    #     label='',
    #     widget=forms.Textarea(attrs={
    #         'rows': '3',
    #         'placeholder': 'Say Something...'
    #     }))

    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {

        }
