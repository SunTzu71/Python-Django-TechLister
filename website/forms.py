from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import PersonalInformation, Education, Experience

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


class PersonalInformationForm(forms.ModelForm):
    class Meta:
        state_list = [
            ('AL', 'Alabama'),
            ('AK', 'Alaska'),
            ('AZ', 'Arizona'),
            ('AR', 'Arkansas'),
            ('CA', 'California'),
            ('CO', 'Colorado'),
            ('CT', 'Connecticut'),
            ('DE', 'Delaware'),
            ('FL', 'Florida'),
            ('GA', 'Georgia'),
            ('HI', 'Hawaii'),
            ('ID', 'Idaho'),
            ('IL', 'Illinois'),
            ('IN', 'Indiana'),
            ('IA', 'Iowa'),
            ('KS', 'Kansas'),
            ('KY', 'Kentucky'),
            ('LA', 'Louisiana'),
            ('ME', 'Maine'),
            ('MD', 'Maryland'),
            ('MA', 'Massachusetts'),
            ('MI', 'Michigan'),
            ('MN', 'Minnesota'),
            ('MS', 'Mississippi'),
            ('MO', 'Missouri'),
            ('MT', 'Montana'),
            ('NE', 'Nebraska'),
            ('NV', 'Nevada'),
            ('NH', 'New Hampshire'),
            ('NJ', 'New Jersey'),
            ('NM', 'New Mexico'),
            ('NY', 'New York'),
            ('NC', 'North Carolina'),
            ('ND', 'North Dakota'),
            ('OH', 'Ohio'),
            ('OK', 'Oklahoma'),
            ('OR', 'Oregon'),
            ('PA', 'Pennsylvania'),
            ('RI', 'Rhode Island'),
            ('SC', 'South Carolina'),
            ('SD', 'South Dakota'),
            ('TN', 'Tennessee'),
            ('TX', 'Texas'),
            ('UT', 'Utah'),
            ('VT', 'Vermont'),
            ('VA', 'Virginia'),
            ('WA', 'Washington'),
            ('WV', 'West Virginia'),
            ('WI', 'Wisconsin'),
            ('WY', 'Wyoming')
        ]

        model = PersonalInformation
        fields = ['recruiter', 'first_name', 'last_name', 'city', 'state',
                  'email', 'phone', 'linked_in', 'about', 'profile_image']

        widgets = {
            'recruiter': forms.CheckboxInput(),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'linked_in': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Linked In'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About yourself'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class AddEducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'})
        }


class AddExperienceForm(forms.ModelForm):
    class Meta:

        start_month = [
            ('...', 'Start Month'),
            ('Jan', 'January'),
            ('Feb', 'February'),
            ('Mar', 'March'),
            ('Apr', 'April'),
            ('May', 'May'),
            ('Jun', 'June'),
            ('Jul', 'July'),
            ('Aug', 'August'),
            ('Sep', 'September'),
            ('Oct', 'October'),
            ('Nov', 'November'),
            ('Dec', 'December')
        ]
        end_month = [
            ('...', 'End Month'),
            ('Jan', 'January'),
            ('Feb', 'February'),
            ('Mar', 'March'),
            ('Apr', 'April'),
            ('May', 'May'),
            ('Jun', 'June'),
            ('Jul', 'July'),
            ('Aug', 'August'),
            ('Sep', 'September'),
            ('Oct', 'October'),
            ('Nov', 'November'),
            ('Dec', 'December')
        ]
        model = Experience
        fields = ['company', 'position', 'start_month', 'start_year', 'end_month', 'end_year',
                  'currently_working', 'task_one', 'task_two', 'task_three', 'task_four', 'task_five', 'task_six',
                  'task_seven', 'task_eight', 'task_nine', 'task_ten', 'order']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'start_month': forms.Select(choices=start_month, attrs={'class': 'form-control'}),
            'start_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Start Year'}),
            'end_month': forms.Select(choices=end_month, attrs={'class': 'form-control'}),
            'end_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'End Year'}),
            'currently_working': forms.CheckboxInput(),
            'task_one': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task one'}),
            'task_two': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task two'}),
            'task_three': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task three'}),
            'task_four': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task four'}),
            'task_five': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task five'}),
            'task_six': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task six'}),
            'task_seven': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task seven'}),
            'task_eight': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task eight'}),
            'task_nine': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task nine'}),
            'task_ten': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task ten'}),
        }
