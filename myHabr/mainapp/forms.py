from django import forms
from .models import BlogPost, Tag


class BlogPostForm(forms.ModelForm):
    """Данная форма работает только с подключенным бутстрапом"""
    class Meta:
        model = BlogPost
        fields = ('title', 'blog', 'body', 'tags')
        tags = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
        )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'blog': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'})
        }

