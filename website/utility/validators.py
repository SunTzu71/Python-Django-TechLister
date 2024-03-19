from django import forms

def validate_title_length(value):
    if len(value) <= 3:
        raise forms.ValidationError("Title must be longer than 3 characters.")

def validate_description_length(value):
    if len(value) <= 5:
        raise forms.ValidationError("Description must be longer than 5 characters.")
