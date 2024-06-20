from django import forms

class BillingDetailsForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    company_name = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100)
    street_address = forms.CharField(max_length=255)
    town_city = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()
    order_notes = forms.CharField(widget=forms.Textarea, required=False)
