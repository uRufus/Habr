from django import forms
from .models import BlogPost, Tag


class BlogPostForm(forms.ModelForm):
    """Данная форма работает только с подключенным бутстрапом"""

    def save(self, commit=True):
        instance = super().save()
        if not instance.tag_list:
            return instance
        tags = instance.tag_list.split()
        if tags:
            for tag in tags:
                if not tag:
                    continue
                tag, _ = Tag.objects.get_or_create(name=tag)
                instance.tags.add(tag)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = BlogPost

        fields = ('title', 'blog', 'body', 'tag_list', 'image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'blog': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tag_list': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }
