from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import MyHabrUser


# Формы регистрации пользователя
class MyHabrUserRegisterForm(UserCreationForm):
    class Meta:
        model = MyHabrUser
        fields = (
            'username', 'first_name', 'password1',
            'password2', 'email'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


# Форма для аутентификации
class MyHabrUserLoginForm(AuthenticationForm):
    class Meta:
        model = MyHabrUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(MyHabrUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
