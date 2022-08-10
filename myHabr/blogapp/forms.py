from django import forms
from .models import Blogs


class MyBlogForm(forms.ModelForm):
    """Данная форма работает только с подключенным бутстрапом"""
    class Meta:
        model = Blogs
        fields = ('category', 'name')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'user_id': forms.Select(attrs={'class': 'form-control'}),

        }

