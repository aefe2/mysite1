from django import forms
from polls.models import User


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин', error_messages={
        'required': 'Обязательное поле',
        'unique': 'Данный логин занят'
    })
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    avatar = forms.ImageField(label='Аватар')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                               error_messages={'required': 'Обязательное поле'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'avatar', 'password')
        enctype = "multipart/form-data"


class EditProfile(forms.ModelForm):
    username = forms.CharField(label='Логин', error_messages={
        'unique': 'Данный логин занят'
    })
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    avatar = forms.ImageField(label='Аватар')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'avatar', 'password')
        enctype = "multipart/form-data"
