from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import PersonalInformation

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class AddProfileInfoForm(forms.ModelForm):
    recruiter = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Recruiter"
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}),
        label=""
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}),
        label=""
    )
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "City", "class": "form-control"}),
        label=""
    )
    state = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "State", "class": "form-control"}),
        label=""
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}),
        label=""
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}),
        label=""
    )
    linked_in = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={"placeholder": "LinkedIn Profile", "class": "form-control"}),
        label=""
    )
    facebook = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={"placeholder": "Facebook Profile", "class": "form-control"}),
        label=""
    )
    about = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "About", "class": "form-control"}),
        label=""
    )
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
        label="Profile Image"
    )

    class Meta:
        model = PersonalInformation
        fields = ['recruiter', 'first_name', 'last_name', 'city', 'state', 'email', 'phone', 'linked_in', 'facebook',
                  'about', 'profile_image']