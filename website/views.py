from PIL import Image
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, AddPersonalInfoForm, AddEducationForm, AddExperienceForm
from .models import PersonalInformation


def home(request):
    return render(request, 'home.html', {})


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            # login user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)

            # todo: create a profile page and redirect user there
            return redirect('home')
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    # The view website.views.register_user didn't return an HttpResponse object. It returned None instead.
    return render(request, 'register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


def add_education(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddEducationForm(request.POST)
            if form.is_valid():
                add_education = form.save(commit=False)
                add_education.user_id = request.user
                add_education.save()
                return redirect('home')
            else:
                return render(request, 'add_education.html', {'form': form})
        else:
            form = AddEducationForm()
            return render(request, 'add_education.html', {'form': form})
    else:
        return redirect('home')


def add_experience(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddExperienceForm(request.POST)

            if form.is_valid():
                add_experience = form.save(commit=False)
                add_experience.user_id = request.user
                add_experience.start_year = int(request.POST['start_year'])
                add_experience.end_year = int(request.POST['end_year'])
                add_experience.save()
                return redirect("home")
            else:
                print(request.POST)
                return render(request, 'add_experience.html', {'form': form})
        else:
            form = AddExperienceForm()
            return render(request, 'add_experience.html', {'form': form})

    else:
        return redirect('home')


def add_personal_info(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddPersonalInfoForm(request.POST, request.FILES)
            if form.is_valid():
                add_personal_info = form.save(commit=False)
                add_personal_info.user_id = request.user

                # Process the image file if it's in the form
                # todo: put this into a utils class - we will be doing more image resizing
                if 'profile_image' in request.FILES:
                    profile_image = request.FILES['profile_image']
                    img = Image.open(profile_image)

                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)

                        # Create a BytesIO object to temporarily hold the resized image
                        from io import BytesIO
                        output_io = BytesIO()

                        # Save the resized image to the BytesIO object
                        img.save(output_io, format=img.format)

                        # Get the file name and extension from the original image
                        file_name = profile_image.name
                        file_ext = file_name.split('.')[-1].lower()

                        # Create a new InMemoryUploadedFile with the resized image data
                        from django.core.files.uploadedfile import InMemoryUploadedFile
                        resized_image = InMemoryUploadedFile(output_io, None, file_name, f'image/{file_ext}',
                                                             output_io.tell(), None)

                        # Assign the resized image to the profile info
                        add_personal_info.profile_image = resized_image

                add_personal_info.save()  # Save the profile info with the resized image
                return redirect('home')
            else:
                return render(request, 'add_personalinfo.html', {'form': form})
        else:
            form = AddPersonalInfoForm()
            return render(request, 'add_personalinfo.html', {'form': form})
    else:
        return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # check if user is a recruiter then redirect to correct template
            try:
                personal_info = PersonalInformation.objects.get(user_id=user)
                is_recruiter = personal_info.recruiter
                if is_recruiter:
                    return redirect('recruiter_profile')
                else:
                    return redirect('user_profile')
            except PersonalInformation.DoesNotExist:
                # there is no personal information for current user so redirect to personal info form
                return redirect('add_personalinfo')
        else:
            messages.error(request, 'Invalid login')
            return redirect('home')
    else:
        return render(request, 'home.html', {})


@login_required
def user_profile(request):
    return render(request, 'user_profile.html', {})


@login_required
def recruiter_profile(request):
    return render(request, 'recruiter_profile.html', {})
