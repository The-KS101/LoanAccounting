from .models import Client, AmountAdded
from django import forms
from django.forms import ModelForm

class SearchBar(forms.Form):
    searchVal = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Enter Account ID...'}))

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'homeAddress', 
        'shopAddress', 'work', 'guarantorName',
        'guarantorAddress', 'guarantorPhone', 'amount']

class SavingsWithdraw(forms.Form):
    amountWithdrawn = forms.IntegerField()

class AmountAddedForm(ModelForm):
    class Meta:
        model = AmountAdded
        fields = ['amountPaid', 'amountSaved',]
        labels = {
            'amountPaid': 'Amount Paid',
            'amountSaved': 'Amount Saved'
        }

class ReturneeForm(ModelForm):
    class Meta:
        model = Client
        fields = ['amount']