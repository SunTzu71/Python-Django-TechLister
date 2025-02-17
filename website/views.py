import os
import secrets
from django.http import Http404
from django.core.mail import send_mail
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from openai import OpenAI
from django.conf import settings
from .forms import RegistrationForm, PersonalInformationForm, AddEducationForm, AddExperienceForm, Portfolio, \
    PortfolioForm, NewJobListingForm, CoverLetterForm, ArticleForm
from .models import (PersonalInformation, Education, Experience, Skill, UserSkill, JobListing, JobSkill,
                     SavedJobs, SavedUsers, User, AppliedJobs, Article, AIToken)
from common.image_resize import image_resize
from common.currency_format import format_currency
from .neural_searcher import NeuralSearcher
from .allviews.verify_user_email import send_verification_email


def home(request):
    return render(request, 'home.html', {})


def job_seeker(request):
    return render(request, 'job_seekers.html')


def business_recruiter(request):
    return render(request, 'business_recruiter.html')


def restricted_access(request):
    return render(request, 'restricted_access.html', {})


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()

            send_verification_email(user)
            new_user_message()
            return redirect('check_email_verify')
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def new_user_message():
    subject = 'TAHub - New User'
    message = 'There is a new users'
    tahub_email = 'chris@techartisanhub.com'

    try:
        send_mail(
            subject,
            message,
            tahub_email,
            [tahub_email],
            fail_silently=False,
        )
    except Exception as e:
        print(e)


def check_email_verify(request):
    return render(request, 'check_email.html', {})


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
def add_education(request):
    if request.method == 'POST':
        form = AddEducationForm(request.POST)
        if form.is_valid():
            add_education = form.save(commit=False)
            add_education.user = request.user
            add_education.save()
            return redirect('edit_resume')
        else:
            return render(request, 'add_education.html', {'form': form})
    else:
        form = AddEducationForm()
    return render(request, 'add_education.html', {'form': form})


@login_required
def edit_education(request, pk):
    try:
        education = Education.objects.get(user=request.user, pk=pk)
        if request.method == 'POST':
            form = AddEducationForm(request.POST, instance=education)
            if form.is_valid():
                form.save()
                return redirect('user_profile')
        else:
            form = AddEducationForm(instance=education)
        return render(request, 'edit_education.html', {'form': form})
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def delete_education(request, pk):
    try:
        delete_education = Education.objects.get(user=request.user, pk=pk)
        delete_education.delete()
        return redirect('edit_resume')
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def add_experience(request):
    if request.method == 'POST':
        form = AddExperienceForm(request.POST)

        if form.is_valid():
            add_experience = form.save(commit=False)
            add_experience.user = request.user
            #add_experience.start_year = int(request.POST['start_year'])
            #add_experience.end_year = int(request.POST['end_year'])
            add_experience.save()
            return redirect('edit_resume')
        else:
            return render(request, 'add_experience.html', {'form': form})
    else:
        form = AddExperienceForm()
    return render(request, 'add_experience.html', {'form': form})


@login_required
def edit_experience(request, pk):
    try:
        edit_experience = Experience.objects.get(user=request.user, pk=pk)
        if request.method == 'POST':
            form = AddExperienceForm(request.POST, instance=edit_experience)
            if form.is_valid():
                form.save()
                return redirect('edit_resume')
        else:
            form = AddExperienceForm(instance=edit_experience)
        return render(request, 'edit_experience.html', {'form': form})
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def delete_experience(request, pk):
    try:
        delete_experience = Experience.objects.get(user=request.user, pk=pk)
        delete_experience.delete()
        return redirect('edit_resume')
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def add_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, is_adding=True)
        print('form')
        print(form)
        if form.is_valid():
            add_portfolio = form.save(commit=False)
            add_portfolio.user = request.user

            if 'portfolio_image' in request.FILES:
                portfolio_image = request.FILES['portfolio_image']
                img = Image.open(portfolio_image)

                # generate image file name
                file_ext = os.path.splitext(portfolio_image.name)[-1].lower()
                rand_img = secrets.token_hex(4)
                user_portfolio_image = str(request.user.id) + '-port-' + rand_img + file_ext

                add_portfolio.portfolio_image = image_resize(img,
                                                             portfolio_image.size,
                                                             400,
                                                             400,
                                                             user_portfolio_image)

            add_portfolio.save()
            return redirect('add_user_portfolio')
        else:
            return render(request, 'add_portfolio.html', {'form': form})
    else:
        # get the form and list of portfolio entries to show under form
        list_portfolio = Portfolio.objects.filter(user_id=request.user)
        context = {'form': PortfolioForm(), 'port_list': list_portfolio}

        return render(request, 'add_portfolio.html', context)


@login_required
def edit_portfolio(request, pk):
    try:
        portfolio = Portfolio.objects.get(user=request.user, pk=pk)
        if request.method == 'POST':
            form = PortfolioForm(request.POST, instance=portfolio, is_adding=False)

            if form.is_valid():
                edit_portfolio = form.save(commit=False)

                if 'portfolio_image' in request.FILES:
                    # delete image on system before uploading new one
                    portfolio.portfolio_image.delete()

                    portfolio_image = request.FILES['portfolio_image']
                    img = Image.open(portfolio_image)

                    # generate image file name
                    file_ext = os.path.splitext(portfolio_image.name)[-1].lower()
                    rand_img = secrets.token_hex(4)
                    user_portfolio_image = str(request.user.id) + '-port-' + rand_img + file_ext

                    edit_portfolio.portfolio_image = image_resize(img,
                                                                  portfolio_image.size,
                                                                  400,
                                                                  400,
                                                                  user_portfolio_image)

                edit_portfolio.save()
                return redirect('add_user_portfolio')
        else:
            form = PortfolioForm(instance=portfolio)
        return render(request, 'edit_portfolio.html', {'form': form})
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def delete_portfolio(request, pk):
    try:
        delete_portfolio = Portfolio.objects.get(user=request.user, pk=pk)
        delete_portfolio.delete()
        return redirect('add_user_portfolio')
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def edit_personal_info(request, pk):
    try:
        personal_info = PersonalInformation.objects.get(user=request.user)
        if request.method == 'POST':
            form = PersonalInformationForm(request.POST, instance=personal_info)
            if form.is_valid():
                edit_personal_info = form.save(commit=False)

                if 'profile_image' in request.FILES:
                    # user updating image so delete the old one from file system
                    if personal_info.profile_image and os.path.isfile(
                            os.path.join(settings.MEDIA_ROOT, personal_info.profile_image.path)):
                        personal_info.profile_image.delete()

                    # upload new image
                    profile_image = request.FILES['profile_image']
                    img = Image.open(profile_image)

                    # get file extension and generate file name
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
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def delete_profile_image(request):
    try:
        personal_info = get_object_or_404(PersonalInformation, user=request.user)

        # delete the old image and update with default image
        personal_info.profile_image.delete()
        personal_info.profile_image = 'images/default-profile.jpeg'
        personal_info.save()
        return render(request, 'messages/profile-image-deleted.html')
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def add_personal_info(request):
    try:
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

                # check if recruiter or user and redirect to profile page
                personal_info = PersonalInformation.objects.get(user=request.user)
                is_recruiter = personal_info.recruiter
                if is_recruiter:
                    request.session['recruiter'] = True
                    return redirect('recruiter_profile')
                else:
                    request.session['recruiter'] = False
                    return redirect('user_profile')

            else:
                return render(request, 'add_personalinfo.html', {'form': form})
        else:
            form = PersonalInformationForm()
            return render(request, 'add_personalinfo.html', {'form': form})
    except ObjectDoesNotExist:
        return redirect('restricted_access')


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
            return render(request, 'user_login_failed.html')
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

    user_instance = get_object_or_404(User, pk=userinfo[0])
    saved_user = SavedUsers.objects.filter(saved=user_instance).first()
    check_user = bool(saved_user)

    context = {'pii': personal_info,
               'resume': resume,
               'saved_user': check_user,
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


@login_required
def delete_job_skill(request, pk):
    try:
        delete_skill = JobSkill.objects.get(pk=pk)

        # Check if logged-in user is the owner of the job listing
        if not request.user == delete_skill.job.user:
            # If current user is not the user who created the job listing then raise permission error.
            raise PermissionDenied

        delete_skill.delete()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def delete_job(request, pk):
    try:
        delete_job = JobListing.objects.get(user=request.user, pk=pk)
        delete_job.delete()
        return redirect('job_listings')
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def skill_search(request):
    skill_input = request.GET.get('skill_input', None)
    skill_results = None

    if skill_input:
        skill_results = Skill.objects.filter(name__icontains=skill_input)
        if skill_results:
            return render(request, 'skill_search.html', {'skills': skill_results})
        else:
            return render(request, 'skill_search.html', {'skill_input': skill_input})


@login_required
@require_POST
def add_skill(request, skill_input):
    skill = Skill.objects.create(name=skill_input)

    # check to see if we have job_id in session if so then we are editing job listing
    job_id = request.session.get('job_id')
    if job_id:
        edit_listing = JobListing.objects.get(pk=job_id)
        JobSkill.objects.create(skill_id=skill.id, skill_name=skill_input, job_id=edit_listing.id)
        return redirect('edit_job', pk=request.session.get('job_id'))

    # Check if they are a recruiter
    if request.session.get('recruiter'):
        if 'job_skills' not in request.session:
            request.session['job_skills'] = []

        job_skills = request.session['job_skills']
        job_skills.append((skill.id, skill_input))
        request.session['job_skills'] = job_skills
        return redirect('add_job_skill')
    else:
        UserSkill.objects.create(skill_id=skill.id, skill_name=skill_input, user_id=request.user.id)
        return redirect('edit_resume')


@login_required
@require_POST
def add_user_skill(request, pk, skill_name):
    # check to see if we have job_id in session if so then we are editing job listing
    job_id = request.session.get('job_id')
    if job_id:
        edit_listing = JobListing.objects.get(pk=job_id)
        JobSkill.objects.create(skill_id=pk, skill_name=skill_name, job_id=edit_listing.id)
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
        UserSkill.objects.create(skill_id=skill_id, skill_name=skill_name, user=request.user)

        return redirect('edit_resume')


@login_required
def delete_user_skill(request, pk):
    try:
        delete_skill = UserSkill.objects.get(user=request.user, pk=pk)
        delete_skill.delete()
        return redirect('edit_resume')
    except ObjectDoesNotExist:
        return redirect('restricted_access')


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
neural_user_search = NeuralSearcher(collection_name='userlistings')


def main_search(request):
    if request.method == 'POST':
        if request.POST.get('searchType') == 'userSearch':
            return user_search(request)
        if request.POST.get('searchType') == 'jobSearch':
            return job_search(request)


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


def user_search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        search_results = neural_user_search.search(text=query)

        context = {'search_results': search_results}

        # Attempt to get first user's resume information
        try:
            first_user = search_results[0]['user_id']
            context['first'] = get_resume_information(first_user)
        except User.DoesNotExist:
            # handle exception
            context['no_results'] = None
            # Make sure to replace the print statement with your desired way of handling exception.
            # The main idea is to ensure your code doesn't break if a user does not exist.
        except IndexError:
            # handle scenario where search_results is empty
            context['no_results'] = None

        return render(request, 'user_listings.html', context)
        # may want to add a no results text and pass it in or check it in the template
    return render(request, 'user_listings.html', {'search_results': []})


@login_required
def save_job(request, pk):
    job, created = SavedJobs.objects.get_or_create(user_id=request.user.id, job_id=pk)
    if created:
        return render(request, 'messages/job-saved.html')
    else:
        return


@login_required
def apply_job(request, pk):
    # get token amount to display AI button
    user_tokens = AIToken.objects.filter(user=request.user).first()
    if user_tokens is None:
        ai_token = AIToken(user=request.user, amount=0)
        ai_token = False
    else:
        ai_token = True

    if request.method == 'POST':
        job = JobListing.objects.get(pk=pk)
        form = CoverLetterForm(request.POST)
        context = {'jobinfo': get_job_information(pk),
                   'userinfo': get_resume_information(request.user.id),
                   'ai_token': ai_token,
                   'form': form}

        if form.is_valid():
            add_letter = form.save(commit=False)
            add_letter.user = request.user
            add_letter.job = job
            add_letter.save()
            return redirect('applied_jobs')
        else:
            return render(request, 'apply_job.html', context)
    else:
        context = {'jobinfo': get_job_information(pk),
                   'userinfo': get_resume_information(request.user.id),
                   'ai_token': ai_token,
                   'form': CoverLetterForm()}
    return render(request, 'apply_job.html', context)


def generate_cover_letter(user_id, job_id):
    # this needs to be placed in the settings file
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    user_instance = get_object_or_404(User, id=user_id)

    job_info = get_job_information(job_id)

    user_applying = user_instance.first_name + ' ' + user_instance.last_name
    recruiter = job_info['pii'].first_name + ' ' + job_info['pii'].last_name
    job_company = job_info['job'].company
    job_description = job_info['job'].description

    prompt = (f"Write me a cover letter that is no longer than 10 sentences. "
              f"User Dear {recruiter} "
              f"The company name is {job_company}. "
              f"Use {user_applying} for Sincerely signature. "
              f"Then paste the job description "
              f"into the input text.\n\nJob Description:\n{job_description}\n\nCover Letter:")

    # Use the new ChatCompletion of OpenAI to generate the cover letter
    response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])

    # Get the generated cover letter from the response
    cover_letter = response.choices[0].message.content.strip()

    user_tokens = AIToken.objects.get(user=user_instance)
    if user_tokens.amount > 0:
        user_tokens.amount = user_tokens.amount - 1
        user_tokens.save()

    return cover_letter


def ai_cover_letter(request, pk):
    generated_cover_letter = generate_cover_letter(request.user.id, pk)
    formated_letter = generated_cover_letter.replace('\n\n', '<br /><br />')
    context = {'cover_letter': formated_letter, 'job_id': pk}

    return render(request, 'ai_cover_letter.html', context)


@login_required
def manual_cover_letter(request, pk):
    form = CoverLetterForm()
    context = {'form': form, 'job_id': pk}

    return render(request, 'manual_cover_letter.html', context)


@login_required
def remove_applied_job(request, pk):
    try:
        remove_applied = AppliedJobs.objects.get(user=request.user, job=pk)
        remove_applied.delete()
        return redirect('applied_jobs')
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def remove_job(request, pk):
    try:
        job_to_remove = SavedJobs.objects.get(job_id=pk, user=request.user)
    except SavedJobs.DoesNotExist:
        return redirect('job_search')  # or some error page
    job_to_remove.delete()
    return render(request, 'messages/job-removed.html')


@login_required
def user_profile_remove_job(request, pk):
    try:
        job_to_remove = SavedJobs.objects.get(user=request.user, job_id=pk)
        job_to_remove.delete()
        return redirect('saved_jobs')
    except ObjectDoesNotExist:
        return redirect('job_search')


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
        # If this raises DoesNotExist exception then request.user is not the owner
        job_owner = JobListing.objects.get(id=jobid, user=request.user)
        del_applied = AppliedJobs.objects.filter(job=jobid, user=userid)
        del_applied.delete()
        return redirect('user_applications')
    except JobListing.DoesNotExist:
        return redirect('restricted_access')


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
    try:
        user_to_remove = SavedUsers.objects.get(saved=pk)
        if request.user == user_to_remove.recruiter:
            user_to_remove.delete()
            return render(request, 'messages/user-removed.html')
        else:
            return redirect('restricted_access')
    except SavedUsers.DoesNotExist:
        raise Http404('User not found.')


@login_required
def rec_remove_resume(request, pk):
    # logic to remove saved resume from recruiter profile
    user_to_remove = get_object_or_404(SavedUsers, saved=pk)
    if request.user == user_to_remove.recruiter:
        user_to_remove.delete()
        return redirect('saved_resumes')
    else:
        return redirect('recruiter_profile')


@login_required
def add_article(request):
    personal_info = PersonalInformation.objects.get(user=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        context = {'pii': personal_info, 'form': form}
        if form.is_valid():
            add_article = form.save(commit=False)
            add_article.user = request.user
            add_article.save()
            return redirect('list_articles')
        else:
            return render(request, 'add_article.html', context)
    else:
        form = ArticleForm()
        context = {'pii': personal_info, 'form': form}
    return render(request, 'add_article.html', context)


@login_required
def edit_article(request, pk):
    try:
        personal_info = PersonalInformation.objects.get(user=request.user)
        article = Article.objects.get(user=request.user, pk=pk)
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            context = {'pii': personal_info, 'form': form, 'article': article}
            if form.is_valid():
                form.save()
                return redirect('list_articles')
        else:
            form = ArticleForm(instance=article)
            context = {'pii': personal_info, 'form': form, 'article': article}
        return render(request, 'edit_article.html', context)
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def list_articles(request):
    personal_info = PersonalInformation.objects.get(user=request.user)
    user_instance = request.user
    all_articles = user_instance.article.all().order_by('created_at')

    context = {'pii': personal_info, 'all_articles': all_articles}

    return render(request, 'list_articles.html', context)


def view_article(request, pk):
    personal_info = PersonalInformation.objects.get(user=request.user)
    view_article = Article.objects.get(user=request.user, pk=pk)

    context = {'pii': personal_info, 'view_article': view_article}

    return render(request, 'view_article.html', context)
