from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Repairs, Car
from django import forms
from django.contrib.auth.models import User

class UserTypeLoginForm(AuthenticationForm):
    user_type = forms.ChoiceField(
        choices=(('customer', 'Customer'), ('mechanic', 'Mechanic')),
        widget=forms.RadioSelect,
        required=True
    )
    

class UserTypeRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    USER_CHOICES = [
        ('client', 'Client'),
        ('mechanic', 'Mechanic'),
    ]

    user_type = forms.ChoiceField(choices=USER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')

        if user_type == 'mechanic':
            raise forms.ValidationError("Mechanics cannot register through this form.")    


class RepairForm(ModelForm):
    class Meta:
        model = Repairs
        fields = '__all__'
        exclude = [
            'serv_mechanic'
        ]
class carForm(ModelForm):
    manufacturer = forms.CharField(max_length=20, label='Producent')
    model = forms.CharField(max_length=20, label='Model')
    year = forms.CharField(max_length=20, label='Rok')
    vin = forms.CharField(max_length=20, label='VIN')
    class Meta:
            model = Car
            fields = '__all__'
