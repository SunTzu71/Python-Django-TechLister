from django import forms


def validate_title_length(value):
    if len(value) <= 3:
        raise forms.ValidationError("Title must be longer than 3 characters.")


def validate_description_length(value):
    if len(value) <= 5:
        raise forms.ValidationError("Description must be longer than 5 characters.")


def validate_first_name(value):
    if not value:
        raise forms.ValidationError("First name is required.")


def validate_last_name(value):
    if not value:
        raise forms.ValidationError("Last name is required.")


def validate_city(value):
    if not value:
        raise forms.ValidationError("City is required.")


def validate_state(value):
    if not value:
        raise forms.ValidationError("State is required.")


def validate_email(value):
    if not value:
        raise forms.ValidationError("Email is required.")


def validate_about(value):
    if len(value) <= 5:
        raise forms.ValidationError("About must be longer than 5 characters.")
