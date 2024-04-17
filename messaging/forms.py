from django import forms
from .models import Message, MessageReply
from common.validators import validate_title_length, validate_description_length


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


class MessageForm(CustomModelForm):
    custom_validators = {
        'subject': [validate_title_length],
        'body': [validate_description_length],
    }

    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Add your message'}),
        }


class ReplyMessageForm(CustomModelForm):
    custom_validators = {
        'body': [validate_description_length],
    }

    class Meta:
        model = MessageReply
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Add your message'}),
        }
