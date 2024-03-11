from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm
from .models import PersonalInformation


def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # todo: create a profile page and redirect user there
            return redirect('home')
        else:
            messages.error(request, 'Invalid login')
            return redirect('home')
    else:
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


def add_profileinfo(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('recruiter'):
                recruiter_check = True
            else:
                recruiter_check = False

            # Put logic here to validate data and strip unwanted characters

            profile_info = PersonalInformation(
                user_id=request.user,
                recruiter=recruiter_check,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                linked_in=request.POST.get('linked_in'),
                facebook=request.POST.get('facebook'),
                about=request.POST.get('about'),
                profile_image=request.POST.get('profile_image'),
            )
            profile_info.save()
            return redirect('home')

        return render(request, 'add_profileinfo.html')
    else:
        # you can add a message here you must be logged in
        return redirect('home')
