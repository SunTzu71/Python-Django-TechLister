from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, AddProfileInfoForm


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
    form = AddProfileInfoForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                profile_info = form.save(commit=False)
                profile_info.user_id = request.user
                profile_info.save()
                return redirect('home')

        return render(request, 'add_profileinfo.html', {'form': form})
    else:
        # you can add a message here you must be logged in
        return redirect('home')
