from PIL import Image
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import RegistrationForm, PersonalInformationForm, AddEducationForm, AddExperienceForm, Portfolio, \
    PortfolioForm, NewJobListingForm
from .models import PersonalInformation, Education, Experience, Skill, UserSkill, JobListing
from.utility.image_resize import image_resize


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

            return redirect('add_personalinfo')
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
                return redirect('user_profile')
            else:
                return render(request, 'add_education.html', {'form': form})
        else:
            form = AddEducationForm()
        return render(request, 'add_education.html', {'form': form})
    else:
        return redirect('home')


def edit_education(request, pk):
    if request.user.is_authenticated:
        education = Education.objects.get(pk=pk)
        if request.method == 'POST':
            form = AddEducationForm(request.POST, instance=education)
            if form.is_valid():
                form.save()
                return redirect('user_profile')
        else:
            form = AddEducationForm(instance=education)
        return render(request, 'edit_education.html', {'form': form})
    else:
        return redirect('home')


def delete_education(request, pk):
    if request.user.is_authenticated:
        delete_education = Education.objects.get(pk=pk)
        delete_education.delete()
        return redirect('user_profile')
    else:
        return redirect('home')


def add_experience(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddExperienceForm(request.POST)

            if form.is_valid():
                add_experience = form.save(commit=False)
                add_experience.user_id = request.user
                #add_experience.start_year = int(request.POST['start_year'])
                #add_experience.end_year = int(request.POST['end_year'])
                add_experience.save()
                return redirect('user_profile')
            else:
                print(request.POST)
                return render(request, 'add_experience.html', {'form': form})
        else:
            form = AddExperienceForm()
        return render(request, 'add_experience.html', {'form': form})

    else:
        return redirect('home')


def edit_experience(request, pk):
    if request.user.is_authenticated:
        edit_experience = Experience.objects.get(pk=pk)
        if request.method == 'POST':
            form = AddExperienceForm(request.POST, instance=edit_experience)
            if form.is_valid():
                form.save()
                return redirect('user_profile')
        else:
            form = AddExperienceForm(instance=edit_experience)
        return render(request, 'edit_experience.html', {'form': form})
    else:
        return redirect('home')


def delete_experience(request, pk):
    if request.user.is_authenticated:
        delete_experience = Experience.objects.get(pk=pk)
        delete_experience.delete()
        return redirect('user_profile')
    else:
        return redirect('home')


def add_portfolio(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PortfolioForm(request.POST, request.FILES, is_adding=True)
            print('form')
            print(form)
            if form.is_valid():
                add_portfolio = form.save(commit=False)
                add_portfolio.user_id = request.user

                if 'portfilio_image' in request.FILES:
                    portfolio_image = request.FILES['portfilio_image']
                    img = Image.open(portfolio_image)

                    add_portfolio.portfolio_image = image_resize(img, portfolio_image.size, 400, 400)

                add_portfolio.save()
                # todo: need to get the recruiter flag redirect to correct profile page
                return redirect('/portfolio/add')

            else:
                return render(request, 'add_portfolio.html', {'form': form})
        else:
            # get the form and list of portfolio entries to show under form
            list_portfolio = Portfolio.objects.filter(user_id=request.user.id)
            context = {'form': PortfolioForm(), 'port_list': list_portfolio}

            return render(request, 'add_portfolio.html', context)
    else:
        return redirect('home')


def edit_portfolio(request, pk):
    if request.user.is_authenticated:

        portfolio = Portfolio.objects.get(pk=pk)
        print(portfolio)
        if request.method == 'POST':
            form = PortfolioForm(request.POST, instance=portfolio, is_adding=False)
            if form.is_valid():
                edit_portfolio = form.save(commit=False)

                if 'portfolio_image' in request.FILES:
                    portfolio_image = request.FILES['portfolio_image']
                    img = Image.open(portfolio_image)

                    edit_portfolio.portfolio_image = image_resize(img, portfolio_image.size, 400, 400)

                edit_portfolio.save()
                return redirect('/portfolio/add')
        else:
            form = PortfolioForm(instance=portfolio)
        return render(request, 'edit_portfolio.html', {'form': form})
    else:
        return redirect('home')


def delete_portfolio(request, pk):
    if request.user.is_authenticated:
        delete_portfolio = Portfolio.objects.get(pk=pk)
        delete_portfolio.delete()
        return redirect('add_user_portfolio')
    else:
        return redirect('home')


def edit_personal_info(request, pk):
    if request.user.is_authenticated:
        personal_info = PersonalInformation.objects.get(id=pk)
        if request.method == 'POST':
            form = PersonalInformationForm(request.POST, instance=personal_info)
            if form.is_valid():
                edit_personal_info = form.save(commit=False)

                if 'profile_image' in request.FILES:
                    profile_image = request.FILES['profile_image']
                    img = Image.open(profile_image)

                    # Assign the resized image to the profile info
                    edit_personal_info.profile_image = image_resize(img, profile_image, 125, 125)

                edit_personal_info.save()
                # todo: need to get the recruiter flag then redirect to correct profile page
                return redirect('user_profile')
            else:
                # form is not valid render again
                return render(request, 'edit_personalinfo.html', {'form': form})

        else:
            form = PersonalInformationForm(instance=personal_info)
            return render(request, 'edit_personalinfo.html', {'form': form})
    else:
        return redirect('home')


def add_personal_info(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PersonalInformationForm(request.POST, request.FILES)
            if form.is_valid():
                add_personal_info = form.save(commit=False)
                add_personal_info.user_id = request.user

                if 'profile_image' in request.FILES:
                    profile_image = request.FILES['profile_image']
                    img = Image.open(profile_image)

                    # Assign the resized image to the profile info
                    add_personal_info.profile_image = image_resize(img, profile_image, 125, 125)

                add_personal_info.save()  # Save the profile info with the resized image

                # check if recruiter or user and redirecto to profile page
                personal_info = PersonalInformation.objects.get(user_id=request.user)
                is_recruiter = personal_info.recruiter
                if is_recruiter:
                    return redirect('recruiter_profile')
                else:
                    return redirect('user_profile')

            else:
                return render(request, 'add_personalinfo.html', {'form': form})
        else:
            form = PersonalInformationForm()
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
                return redirect('user_profile')
        else:
            messages.error(request, 'Invalid login')
            return redirect('home')
    else:
        return render(request, 'home.html', {})


@login_required
def user_profile(request):
    user_id = request.user.id
    try:
        personal_info = PersonalInformation.objects.get(user_id=user_id)
        education_info = Education.objects.filter(user_id=user_id)
        experience_info = Experience.objects.filter(user_id=user_id)
        user_skills = UserSkill.objects.filter(user_id=user_id)

        context = {'pii': personal_info,
                   'edus': education_info,
                   'exps': experience_info,
                   'uskills': user_skills}

    except PersonalInformation.DoesNotExist:
        return redirect('add_personalinfo')

    return render(request, 'user_profile.html',  context)


def user_resume(request, pk):
    try:
        personal_info = PersonalInformation.objects.get(user_id=pk)
        education_info = Education.objects.filter(user_id=pk)
        experience_info = Experience.objects.filter(user_id=pk)
        user_skills = UserSkill.objects.filter(user_id=pk)

        context = {'pii': personal_info,
                   'edus': education_info,
                   'exps': experience_info,
                   'uskills': user_skills}

    except PersonalInformation.DoesNotExist:
        return redirect('user_profile')

    return render(request, 'user_resume.html', context)



@login_required
def recruiter_profile(request):
    return render(request, 'recruiter_profile.html', {})


def add_job(request):
    if request.user.is_authenticated:
        # todo: check to make sure they are a recruiter
        if request.method == 'POST':
            form = NewJobListingForm(request.POST)
            if form.is_valid():
                add_listing = form.save(commit=False)
                add_listing.user_id = request.user
                add_listing.save()
                return redirect('recruiter_profile')
            else:
                return render(request, 'add_joblisting.html', {'form': form})
        else:
            form = NewJobListingForm()
        return render(request, 'add_joblisting.html', {'form': form})
    else:
        return redirect('home')


@login_required
def skill_search(request):
    skill_input = request.GET.get('skill_input', None)
    skill_results = None

    if skill_input:
        skill_results = Skill.objects.filter(skill__icontains=skill_input)
        if skill_results:
            print(skill_results)
            return render(request, 'skill_search.html', {'skills': skill_results})
        else:
            # todo: need a better way to add skill when not found
            return render(request, 'skill_search.html', {'skill_input': skill_input})


@login_required
@require_POST
def add_skill(request, skill_input):
    # todo: need to sanitize the data
    skill = Skill.objects.create(skill=skill_input)
    UserSkill.objects.create(skill_id=skill.id, skill_name=skill_input, user_id=request.user)

    return redirect('user_profile')


@login_required
@require_POST
def add_user_skill(request, pk, skill_name):
    skill_id = pk
    user_id = request.user
    UserSkill.objects.create(skill_id=skill_id, skill_name=skill_name, user_id=user_id)

    return redirect('user_profile')


@login_required
def delete_user_skill(request, pk):
    if request.user.is_authenticated:
        delete_skill = UserSkill.objects.get(pk=pk)
        delete_skill.delete()
        return redirect('user_profile')
    else:
        return redirect('home')
