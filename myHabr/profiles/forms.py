from django import forms
from .models import Profile

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='Имя: ')
    last_name = forms.CharField(max_length=50, label='Фамилия: ')
    age = forms.IntegerField(max_value=150, label='Возраст: ')
    text = forms.CharField(widget=forms.Textarea, label='О себе: ')

    def form_initial(self, id):
        # Пытаюсь в цикле поставить значение элемента формы initial из БД НЕ ПОЛУЧАЕТСЯ
        obj = Profile.objects.in_bulk()
        obj = obj[id]

        for k, v in self.fields.items():
            print(self.fields[k].initial)
            print(obj)


# class ProfileForm(forms.Form):
#     class Meta:
#         model = Profile
#         fields = ('user_id', 'first_name', 'last_name', 'age', 'text')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.fields['user_id'].widget = forms.HiddenInput()
#         for name, field in self.fields.items():
#             if name == 'text':
#                 field.widget = forms.Textarea()
#             if name == 'user_id':
#                 field.widget = forms.HiddenInput()
#
#     def form_initial(self, obj):
#         for name, field in self.fields.items():
#             field.initial = obj.name



