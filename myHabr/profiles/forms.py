from django import forms
from .models import Profile


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='Имя: ', required=False)
    last_name = forms.CharField(max_length=50, label='Фамилия: ', required=False)
    age = forms.IntegerField(max_value=150, label='Возраст: ', required=False)
    text = forms.CharField(widget=forms.Textarea, label='О себе: ', required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    def form_initial(self, id):
        # Пытаюсь в цикле поставить значение элемента формы initial из БД НЕ ПОЛУЧАЕТСЯ
        obj = Profile.objects.in_bulk([id])

        for k, v in self.fields.items():
            for id_ob in obj:
                self.fields[k].initial = obj[id_ob][k]
