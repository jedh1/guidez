from django import forms

spc_rates = (
    ('','None'),
    ('1','Corporate, Promo, SET#'),
    ('2', 'AAA, CAA'),
    ('3', 'Senior Discount'),
    ('4', 'Government & Military')
)

class SearchForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=False)
    email_box = forms.BooleanField(label='Send results to email?', required=False)
    email_freq = forms.IntegerField(label='Results will be emailed once every this many days:', max_value=50, required=False)
    destination = forms.CharField(label='Destination', widget=forms.TextInput())
    cin_date = forms.CharField(label='Check-in Date', widget=forms.TextInput())
    cout_date = forms.CharField(label='Check-out Date', widget=forms.TextInput())
    special_rates = forms.ChoiceField(choices=spc_rates, required=False)
    special_rates_code = forms.CharField(label='Corporate / Promo / SET #', widget=forms.TextInput(), required=False)
