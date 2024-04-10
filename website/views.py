import os
from django.http import Http404
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from .forms import RegistrationForm, PersonalInformationForm, AddEducationForm, AddExperienceForm, Portfolio, \
    PortfolioForm, NewJobListingForm, CoverLetterForm
from .models import (PersonalInformation, Education, Experience, Skill, UserSkill, JobListing, JobSkill,
                     SavedJobs, SavedUsers, User, AppliedJobs)
from .utility.image_resize import image_resize
from .utility.currency_format import format_currency
from .neural_searcher import NeuralSearcher
from .allviews.verify_user_email import send_verification_email, verify_email


def home(request):
    return render(request, 'home.html', {})


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False;
            user.save()
            send_verification_email(user)
            return redirect('home')
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
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
                add_education.user = request.user
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
                add_experience.user = request.user
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
                add_portfolio.user = request.user

                if 'portfilio_image' in request.FILES:
                    portfolio_image = request.FILES['portfilio_image']
                    img = Image.open(portfolio_image)

                    add_portfolio.portfolio_image = image_resize(img, portfolio_image.size, 400, 400)

                add_portfolio.save()
                return redirect('add_user_portfolio')
            else:
                return render(request, 'add_portfolio.html', {'form': form})
        else:
            # get the form and list of portfolio entries to show under form
            list_portfolio = Portfolio.objects.filter(user_id=request.user)
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
                return redirect('add_user_portfolio')
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


@login_required
def edit_personal_info(request, pk):
    if request.user.is_authenticated:
        # todo: we need to check to make sure the user is the owner to edit
        personal_info = PersonalInformation.objects.get(user_id=pk)
        if request.method == 'POST':
            form = PersonalInformationForm(request.POST, instance=personal_info)
            if form.is_valid():
                edit_personal_info = form.save(commit=False)

                if 'profile_image' in request.FILES:
                    # user updating image so delete the old one from file system
                    personal_info.profile_image.delete()

                    # upload new image
                    profile_image = request.FILES['profile_image']
                    img = Image.open(profile_image)

                    file_ext = os.path.splitext(profile_image.name)[-1].lower()
                    user_profile_image = request.user.username + '-profile' + file_ext

                    # Assign the resized image to the profile info
                    edit_personal_info.profile_image = image_resize(img, profile_image, 125, 125, user_profile_image)

                edit_personal_info.save()

                if personal_info.recruiter:
                    return redirect('recruiter_profile')
                else:
                    return redirect('user_profile')
            else:
                # form is not valid render again
                return render(request, 'edit_personalinfo.html', {'form': form})

        else:
            form = PersonalInformationForm(instance=personal_info)
            return render(request, 'edit_personalinfo.html', {'form': form})
    else:
        return redirect('home')


@login_required
def delete_profile_image(request):
    if request.user.is_authenticated:
        personal_info = get_object_or_404(PersonalInformation, user_id=request.user.id)

        # delete the old image and update with default image
        personal_info.profile_image.delete()
        personal_info.profile_image = 'images/default-profile.jpeg'

        personal_info.save()

    return render(request, 'messages/profile-image-deleted.html')


@login_required
def add_personal_info(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PersonalInformationForm(request.POST, request.FILES)
            if form.is_valid():
                add_personal_info = form.save(commit=False)
                add_personal_info.user = request.user

                if 'profile_image' in request.FILES:
                    profile_image = request.FILES['profile_image']
                    img = Image.open(profile_image)

                    file_ext = os.path.splitext(profile_image.name)[-1].lower()
                    user_profile_image = request.user.username + '_' + file_ext

                    # Assign the resized image to the profile info
                    add_personal_info.profile_image = image_resize(img, profile_image, 125, 125, user_profile_image)

                add_personal_info.save()  # Save the profile info with the resized image

                # check if recruiter or user and redirecto to profile page
                personal_info = PersonalInformation.objects.get(user=request.user)
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


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'user_login.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # check if user is a recruiter then redirect to correct template
            try:
                personal_info = PersonalInformation.objects.get(user=user)
                is_recruiter = personal_info.recruiter
                if is_recruiter:
                    request.session['recruiter'] = True
                    return redirect('recruiter_profile')
                else:
                    request.session['recruiter'] = False
                    return redirect('user_profile')
            except PersonalInformation.DoesNotExist:
                # there is no personal information for current user so redirect to personal info form
                return redirect('add_personalinfo')
        else:
            messages.error(request, 'Invalid login')
            return redirect('home')
    else:
        return render(request, 'home.html', {})


def get_resume_information(pk):
    try:
        user_info = User.objects.get(id=pk)
        personal_info = PersonalInformation.objects.get(user_id=pk)
        education_info = Education.objects.filter(user_id=pk)
        experience_info = Experience.objects.filter(user_id=pk)
        user_skills = UserSkill.objects.filter(user_id=pk)
        saved_user = SavedUsers.objects.filter(saved=pk).first()
        check_user = bool(saved_user)

        context = {'pii': personal_info,
                   'userinfo': user_info,
                   'edus': education_info,
                   'exps': experience_info,
                   'saved_user': check_user,
                   'uskills': user_skills}

        return context

    except PersonalInformation.DoesNotExist:
        return None


def user_resume(request, pk):
    context = get_resume_information(pk)

    if not context:
        return redirect('user_profile')

    return render(request, 'user_resume.html', context)


def user_page(request, username):
    userinfo = User.objects.filter(username=username).values_list('id', 'username').first()
    personal_info = PersonalInformation.objects.get(user_id=userinfo[0])
    resume = get_resume_information(userinfo[0])

    context = {'pii': personal_info,
               'resume': resume,
               'username': userinfo[1]}

    return render(request, 'user_page/user_home.html', context)


def user_portfolio(request, username):
    userinfo = User.objects.filter(username=username).values_list('id', 'username').first()
    personal_info = PersonalInformation.objects.get(user_id=userinfo[0])
    list_portfolio = Portfolio.objects.filter(user_id=userinfo[0])

    context = {'pii': personal_info,
               'portfolio': list_portfolio,
               'username': userinfo[1]}

    return render(request, 'user_page/portfolio.html', context)


def all_resume(request, pk):
    context = get_resume_information(pk)

    if not context:
        return redirect('user_profile')

    return render(request, 'all_resume.html', context)


def add_job_skill(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = NewJobListingForm(request.POST)
                if form.is_valid():
                    add_listing = form.save(commit=False)
                    add_listing.user_id = request.user
                    add_listing.save()
                    return redirect('recruiter_profile')
                else:
                    return render(request, 'add_joblisting_skill.html', {'form': form})
            else:
                form = NewJobListingForm()
            return render(request, 'add_joblisting_skill.html', {'form': form})
        else:
            return redirect('home')


def add_job(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = NewJobListingForm(request.POST)
            if form.is_valid():
                add_listing = form.save(commit=False)
                add_listing.user = request.user
                add_listing.save()

                # loop through job skills and insert into database
                for skill in request.session['job_skills']:
                    JobSkill.objects.create(skill_id=skill[0], skill_name=skill[1], job_id=add_listing)

                # delete session holding the job skills
                del request.session['job_skills']

                return redirect('recruiter_profile')
            else:
                return render(request, 'add_joblisting.html', {'form': form})
        else:
            form = NewJobListingForm()
        return render(request, 'add_joblisting.html', {'form': form})
    else:
        return redirect('home')


def edit_job(request, pk):
    if request.user.is_authenticated:
        # add job listing id to session
        # this is used in add_user_skill method
        request.session['job_id'] = pk

        edit_listing = JobListing.objects.get(id=pk)
        if request.method == 'POST':
            form = NewJobListingForm(request.POST, instance=edit_listing)
            if form.is_valid():
                form.save()

                # remove job_id from request session
                del request.session['job_id']
                return redirect('recruiter_profile')
        else:
            skills = JobSkill.objects.filter(job_id=edit_listing.id)
            context = {'form': NewJobListingForm(instance=edit_listing),
                       'jskills': skills}

        return render(request, 'edit_joblisting.html', context)
    else:
        return redirect('home')


@login_required
def delete_job_skill(request, pk):
    if request.user.is_authenticated:
        delete_skill = JobSkill.objects.get(pk=pk)
        delete_skill.delete()

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)
    else:
        return redirect('home')


def delete_job(request, pk):
    if request.user.is_authenticated:
        delete_job = JobListing.objects.get(pk=pk)
        delete_job.delete()
        return redirect('recruiter_profile')
    else:
        return redirect('home')


@login_required
def skill_search(request):
    skill_input = request.GET.get('skill_input', None)
    skill_results = None

    if skill_input:
        skill_results = Skill.objects.filter(skill__icontains=skill_input)
        if skill_results:
            return render(request, 'skill_search.html', {'skills': skill_results})
        else:
            return render(request, 'skill_search.html', {'skill_input': skill_input})


@login_required
@require_POST
def add_skill(request, skill_input):
    skill = Skill.objects.create(skill=skill_input)
    UserSkill.objects.create(skill_id=skill.id, skill_name=skill_input, user_id=request.user)

    return redirect('user_profile')


@login_required
@require_POST
def add_user_skill(request, pk, skill_name):
    # check to see if we have job_id in session if so then we are editing job listing
    job_id = request.session.get('job_id')
    if job_id:
        edit_listing = JobListing.objects.get(pk=job_id)
        JobSkill.objects.create(skill_id=pk, skill_name=skill_name, job_id=edit_listing)
        return redirect('edit_job', pk=request.session.get('job_id'))

    # When recruiter adds a skill it's stored in session
    # logic in if condition used for adding new job listing add_job method
    elif request.session.get('recruiter'):
        if 'job_skills' not in request.session:
            request.session['job_skills'] = []

        job_skills = request.session['job_skills']
        job_skills.append((pk, skill_name))
        request.session['job_skills'] = job_skills

        return redirect('add_job_skill')
    else:
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


def get_job_information(pk):
    try:
        job_info = JobListing.objects.get(id=pk)
        job_skills = JobSkill.objects.filter(job_id=job_info.id)
        saved_job = SavedJobs.objects.filter(job_id=job_info.id).first()
        check_job = bool(saved_job)
        personal_info = PersonalInformation.objects.get(user_id=job_info.user_id)
        job_info.pay_top = format_currency(job_info.pay_top)
        job_info.pay_bottom = format_currency(job_info.pay_bottom)
        context = {'pii': personal_info,
                   'job': job_info,
                   'saved_job': check_job,
                   'skills': job_skills}
        return context

    except JobListing.DoesNotExist:
        return None


def view_job(request, pk):
    try:
        job = get_job_information(pk)
    except ObjectDoesNotExist:
        raise Http404("Job not found")

    if request.user.is_authenticated:
        try:
            applied_job = AppliedJobs.objects.get(user=request.user, job=pk)
            applied_job = True
        except ObjectDoesNotExist:
            applied_job = False

        context = {'jobinfo': job, 'applied': applied_job}
    else:
        context = {'jobinfo': job}

    return render(request, 'view_job.html', context)


@login_required
def all_view_job(request, pk):
    try:
        job = get_job_information(pk)
    except ObjectDoesNotExist:
        raise Http404("Job not found")

    try:
        applied_job = AppliedJobs.objects.get(user=request.user, job=pk)
        applied_job = True
    except ObjectDoesNotExist:
        applied_job = False

    context = {'jobinfo': job, 'applied': applied_job}

    return render(request, 'all_view_job.html', context)


neural_job_search = NeuralSearcher(collection_name='joblistings')


def job_search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        search_results = neural_job_search.search(text=query)

        # need to check if logged in was getting null error because of anonymous user has no id
        if request.user.is_authenticated:
            applied_job_ids = AppliedJobs.objects.filter(user=request.user).values_list('job', flat=True)

            for job in search_results:
                if job['id'] in applied_job_ids:
                    job['applied'] = True
                else:
                    job['applied'] = False

        # get the first element from the json result
        first_job = search_results[0]['id']

        # check if logged in to handle applied jobs logic
        if request.user.is_authenticated:
            try:
                applied_job = AppliedJobs.objects.get(user=request.user, job=first_job)
                applied_job = True
            except ObjectDoesNotExist:
                applied_job = False
            context = {'search_results': search_results,
                       'first': get_job_information(first_job),
                       'applied': applied_job}
        else:
            context = {'search_results': search_results,
                       'first': get_job_information(first_job)}

        return render(request, 'job_listings.html', context)
    return render(request, 'job_listings.html', {'search_results': []})


@login_required
def save_job(request, pk):
    job, created = SavedJobs.objects.get_or_create(user_id=request.user, job_id=pk)
    if created:
        return render(request, 'messages/job-saved.html')
    else:
        return


@login_required
def apply_job(request, pk):
    if request.method == 'POST':
        job = JobListing.objects.get(pk=pk)
        form = CoverLetterForm(request.POST)
        context = {'jobinfo': get_job_information(pk),
                   'userinfo': get_resume_information(request.user.id),
                   'form': form}
        if form.is_valid():
            add_letter = form.save(commit=False)
            add_letter.user = request.user
            add_letter.job = job
            add_letter.save()
            return redirect('user_profile')
        else:
            return render(request, 'apply_job.html', context)
    else:
        context = {'jobinfo': get_job_information(pk),
                   'userinfo': get_resume_information(request.user.id),
                   'form': CoverLetterForm()}
    return render(request, 'apply_job.html', context)


@login_required
def remove_job(request, pk):
    job_to_remove = get_object_or_404(SavedJobs, job_id=pk)

    # checking if the logged-in user is the same who wants to delete the job
    if request.user == job_to_remove.user_id:
        job_to_remove.delete()
        return render(request, 'messages/job-removed.html')
    else:
        return redirect('home')


@login_required
def user_profile_remove_job(request, pk):
    job_to_remove = get_object_or_404(SavedJobs, job_id=pk)

    # checking if the logged-in user is the same who wants to delete the job
    if request.user == job_to_remove.user_id:
        job_to_remove.delete()
        return redirect('saved_jobs')
    else:
        return redirect('home')


@login_required
def view_cover_letter(request, jobid, userid):

    personal_info = PersonalInformation.objects.get(user=userid)
    applied_jobs = AppliedJobs.objects.select_related('user').get(job_id=jobid, user_id=userid)
    resume = get_resume_information(userid)

    context = {'pii': personal_info,
               'aj': applied_jobs,
               'ur': resume}

    if applied_jobs:
        return render(request, 'view_cover_letter.html', context)
    else:
        return redirect('recruiter_profile')


@login_required
def rec_delete_applied(request, jobid, userid):
    try:
        job_owner = JobListing.objects.get(id=jobid, user=request.user)
        del_applied = AppliedJobs.objects.filter(job=jobid, user=userid)
        del_applied.delete()
        return redirect('recruiter_profile')

    except JobListing.DoesNotExist:
        return redirect('home')


@login_required
def save_user(request, pk):
    user_instance = get_object_or_404(User, pk=pk)
    user, created = SavedUsers.objects.get_or_create(
        recruiter=request.user,
        saved=user_instance)

    if created:
        return render(request, 'messages/user-saved.html')
    else:
        return


@login_required
def remove_user(request, pk):
    # logic to remove saved resume on user list search and resume page
    user_to_remove = get_object_or_404(SavedUsers, saved=pk)
    # checking if the logged-in user is the same who wants to delete the job
    if request.user == user_to_remove.recruiter:
        user_to_remove.delete()
        return render(request, 'messages/user-removed.html')
    else:
        return


def rec_remove_resume(request, pk):
    # logic to remove saved resume from recruiter profile
    user_to_remove = get_object_or_404(SavedUsers, saved=pk)
    if request.user == user_to_remove.recruiter:
        user_to_remove.delete()
        return redirect('recruiter_profile')
    else:
        return redirect('recruiter_profile')


neural_user_search = NeuralSearcher(collection_name='userlistings')


def user_search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        search_results = neural_user_search.search(text=query)

        # get the first element from the json result
        first_user = search_results[0]['user_id']
        context = {'search_results': search_results,
                   'first': get_resume_information(first_user)}

        return render(request, 'user_listings.html', context)
        # may want to add a no results text and pass it in or check it in the template
    return render(request, 'user_listings.html', {'search_results': []})
