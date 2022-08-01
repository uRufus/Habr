from django import forms
from .models import Profile

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='Имя: ')
    last_name = forms.CharField(max_length=50, label='Фамилия: ')
    age = forms.IntegerField(max_value=150, label='Возраст: ')
    text = forms.CharField(widget=forms.Textarea, label='О себе: ')

    def form_initial(self, id):
        # Пытаюсь в цикле поставить значение элемента формы initial из БД НЕ ПОЛУЧАЕТСЯ
        obj = Profile.objects.in_bulk([id])

        for k, v in self.fields.items():
            for id_ob in obj:
                self.fields[k].initial = obj[id_ob][k]





