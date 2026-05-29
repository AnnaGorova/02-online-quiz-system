from django import forms

class UsernameForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Ваше ім'я",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть ваше ім\'я',
            'required': True
        })
    )
