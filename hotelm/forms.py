from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

spc_rates = (
    ('','None'),
    ('1','Corporate, Promo, SET#'),
    ('2', 'AAA, CAA'),
    ('3', 'Senior Discount'),
    ('4', 'Government & Military')
)

class SearchForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    email_freq = forms.IntegerField(label='Send results for (0-30) days: (Optional)', min_value=0, max_value=30, required=False)
    destination = forms.CharField(label='Destination', widget=forms.TextInput())
    cin_date = forms.CharField(label='Check-in Date', widget=forms.TextInput())
    cout_date = forms.CharField(label='Check-out Date', widget=forms.TextInput())
    special_rates = forms.ChoiceField(label= 'Special rates (Optional)', choices=spc_rates, required=False)
    special_rates_code = forms.CharField(label='Corporate / Promo / SET # (Optional)', widget=forms.TextInput(), required=False)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    email = forms.EmailField(required=True, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2',)

class CommentForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField(widget=forms.TextInput())
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
