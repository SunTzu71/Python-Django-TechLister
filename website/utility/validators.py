from django import forms


def validate_title_length(value):
    if not value:
        raise forms.ValidationError("Title is required.")


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


def validate_company(value):
    if not value:
        raise forms.ValidationError("Company is required.")


def validate_position(value):
    if not value:
        raise forms.ValidationError("Position is required.")


def validate_start_month(value):
    if not value:
        raise forms.ValidationError("Start month is required.")


def validate_start_year(value):
    if not value:
        raise forms.ValidationError("Start year is required.")
    if not isinstance(value, int):
        raise forms.ValidationError("Start year must be an integer.")
    if len(str(value)) != 4:
        raise forms.ValidationError("Start year must be exactly 4 characters long.")


def validate_task_one(value):
    if not value:
        raise forms.ValidationError("You need at least one task.")


def validate_website_link(value):
    if not value:
        raise forms.ValidationError("Website link is required.")


def validate_portfolio_image(value):
    if not value:
        raise forms.ValidationError("Portfolio image is required.")
