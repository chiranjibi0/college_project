from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.Form):
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField(min_value=18)
    user_type = forms.ChoiceField(choices=[
        ('admin', 'Admin'),
        ('candidate', 'Candidate'),
        ('voter', 'Voter'),
    ])

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits")
        if User.objects.filter(username=phone).exists():
            raise forms.ValidationError("Phone already registered")
        return phone

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned
