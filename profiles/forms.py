from django import forms
from django.contrib.auth.forms import UserCreationForm
from profiles.models import User
from django.core.exceptions import ValidationError 
from .models import Employee, Invoice, Credit, Analytics
 
class UserRegistrationForm(UserCreationForm):
    MONTH_ABBREVIATIONS = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',
        'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'
    ]
    MONTH_CHOICES = list(enumerate(MONTH_ABBREVIATIONS, 1))
    YEAR_CHOICES = [(i, i) for i in range(2015, 2036)]
 
    credit_card_number = forms.CharField(label='Credit card number')
    cvv = forms.CharField(label='Security code (CVV)')
    expiry_month = forms.ChoiceField(label="Month", choices=MONTH_CHOICES)
    expiry_year = forms.ChoiceField(label="Year", choices=YEAR_CHOICES)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
 
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )
 
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        exclude = ['username']
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            message = "Passwords do not match"
            raise ValidationError(message)
 
        return password2
 
    def save(self, commit=True):
        instance = super(UserRegistrationForm, self).save(commit=False)
 
        # automatically set to email address to create a unique identifier
        instance.username = instance.email
 
        if commit:
            instance.save()
 
        return instance

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class EmployeeForm(forms.ModelForm):
 
    class Meta:
        model = Employee
        exclude = ['user']
        fields = ('name', 'contact','social_security', 'job_title', 'weekly_salary')   

class delete_EmployeeForm(forms.ModelForm):
 
    class Meta:
        model = Employee
        exclude = ['user']
        fields = ('name','social_security')     

class InvoiceForm(forms.ModelForm):
 
    class Meta:
        model = Invoice
        exclude = ['user']
        fields = ('name', 'invoice_type', 'invoice_reference', 'invoice_type', 'payment_frequency', 'amount')

class delete_InvoiceForm(forms.ModelForm):
 
    class Meta:
        model = Invoice
        exclude = ['user']
        fields = ('name','invoice_reference')   

class CreditForm(forms.ModelForm):
 
    class Meta:
        model = Credit
        exclude = ['user']
        fields = ('name', 'payment_reference', 'amount', 'payment_type', 'country', 'payment_location')

class delete_CreditForm(forms.ModelForm):
 
    class Meta:
        model = Credit
        exclude = ['user']
        fields = ('name','payment_reference')  

class AnalyticsForm(forms.ModelForm):
 
    class Meta:
        model = Analytics
        exclude = ['user']
        fields = ('clicks', 'impressions','conversions', 'sales', 'site')       