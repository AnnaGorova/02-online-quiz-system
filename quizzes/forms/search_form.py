from django import forms

class SearchForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=False,
        label="Ім'я для пошуку",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть ім\'я'
        })
    )
