from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import (PersonalInformation, Education, Experience, Portfolio,
                     JobListing, AppliedJobs, Article, UserSkill, JobSkill)

from common.validators import (validate_title_length, validate_description_length, validate_first_name,
                                          validate_last_name, validate_city, validate_state, validate_email,
                                          validate_about, validate_company, validate_position, validate_start_month,
                                          validate_start_year, validate_task_one, validate_website_link,
                                          validate_portfolio_image, validate_job_type, validate_location)


class CustomModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_custom_validators()

    def add_custom_validators(self):
        # Add validators to specific fields
        for field_name, validators in self.custom_validators.items():
            field = self.fields.get(field_name)
            if field:
                field.validators.extend(validators)


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


class PersonalInformationForm(CustomModelForm):
    custom_validators = {
        'first_name': [validate_first_name],
        'last_name': [validate_last_name],
        'city': [validate_city],
        'state': [validate_state],
        'email': [validate_email],
        'about': [validate_about],
    }

    class Meta:
        state_list = [
            ('', 'Select State'),
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
        fields = ['recruiter', 'active', 'first_name', 'last_name', 'city', 'state',
                  'email', 'phone', 'linked_in', 'about', 'profile_image']

        widgets = {
            'recruiter': forms.CheckboxInput(),
            'active': forms.CheckboxInput(),
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


class AIPersonalAboutForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = ['about']

        widgets = {
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class AddEducationForm(CustomModelForm):
    custom_validators = {
        'title': [validate_title_length],
        'description': [validate_description_length],
    }

    class Meta:
        model = Education
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'},),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'})
        }


class CoverLetterForm(forms.ModelForm):
    class Meta:
        model = AppliedJobs
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UserSkillForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields = ['skill_name']
        widgets = {
            'skill_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class JobSkillForm(forms.ModelForm):
    class Meta:
        model = JobSkill
        fields = ['skill_name']
        widgets = {
            'skill_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ArticleForm(forms.ModelForm):
    custom_validators = {
        'title': [validate_title_length],
        'description': [validate_description_length],
    }

    class Meta:
        model = Article
        fields = ['draft', 'title', 'description']
        widgets = {
            'draft': forms.CheckboxInput(),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Description'}),
        }


class PortfolioForm(CustomModelForm):
    custom_validators = {
        'title': [validate_title_length],
        'description': [validate_description_length],
        'website_link': [validate_website_link],
    }

    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'website_link', 'portfolio_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Description'}),
            'website_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website Link'}),
            'portfolio_image': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        self.is_adding = kwargs.pop('is_adding', True)
        super(PortfolioForm, self).__init__(*args, **kwargs)

        if self.is_adding:
            # If adding new entry, apply the image validation
            self.custom_validators['portfolio_image'] = [validate_portfolio_image]
        else:
            # If editing existing entry, remove the image validation
            self.fields['portfolio_image'].required = False

    def clean_portfolio_image(self):
        portfolio_image = self.cleaned_data.get('portfolio_image')

        if self.is_adding and not portfolio_image:
            raise forms.ValidationError("Portfolio image is required when adding portfolio.")

        return portfolio_image


class AddExperienceForm(CustomModelForm):
    custom_validators = {
        'company': [validate_company],
        'position': [validate_position],
        'start_month': [validate_start_month],
        'start_year': [validate_start_year],
        'task_one': [validate_task_one]
    }

    class Meta:

        start_month = [
            ('', 'Start Month'),
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
            ('', 'End Month'),
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


class NewJobListingForm(CustomModelForm):
    custom_validators = {
        'title': [validate_title_length],
        'company': [validate_company],
        'city': [validate_city],
        'state': [validate_state],
        'job_type': [validate_job_type],
        'location': [validate_location],
        'about': [validate_about],
    }

    class Meta:
        state_list = [
            ('', 'Select State'),
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

        job_type_choices = [
            ('', 'Select Job Type'),
            ('full-time', 'Full Time'),
            ('part-time', 'Part time'),
            ('contract', 'Contract'),
            ('intern', 'Intern'),
            ('other', 'Other'),
        ]

        job_location_choices = [
            ('', 'Select Job Location'),
            ('onsite', 'On Site'),
            ('remote', 'Remote'),
            ('hybrid', 'Hybrid'),
        ]

        pay_amount_choices = [
            ('', 'Select Pay Amount'),
            ('40000', '40,000'),
            ('50000', '50,000'),
            ('60000', '60,000'),
            ('70000', '70,000'),
            ('80000', '80,000'),
            ('90000', '90,000'),
            ('100000', '100,000'),
            ('110000', '110,000'),
            ('120000', '120,000'),
            ('130000', '130,000'),
            ('140000', '140,000'),
            ('150000', '150,000'),
            ('160000', '160,000'),
            ('170000', '170,000'),
            ('180000', '180,000'),
            ('190000', '190,000'),
            ('200000', '200,000'),
        ]

        model = JobListing
        fields = ['active', 'title', 'company', 'city', 'state', 'job_type', 'location', 'pay_bottom', 'pay_top',
                  'description']
        widgets = {
            'active': forms.CheckboxInput(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(choices=state_list, attrs={'class': 'form-control'}),
            'job_type': forms.Select(choices=job_type_choices, attrs={'class': 'form-control'}),
            'location': forms.Select(choices=job_location_choices, attrs={'class': 'form-control'}),
            'pay_bottom': forms.Select(choices=pay_amount_choices, attrs={'class': 'form-control'}),
            'pay_top': forms.Select(choices=pay_amount_choices, attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
