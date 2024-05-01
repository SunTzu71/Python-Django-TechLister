from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from website.forms import NewJobListingForm
from website.models import JobSkill
from website.models import SavedUsers, PersonalInformation, JobListing, AppliedJobs
from messaging.views import user_list_messages

from website.forms import JobSkillForm


@login_required
def add_job(request):
    try:
        if request.method == 'POST':
            form = NewJobListingForm(request.POST)
            if form.is_valid():
                add_listing = form.save(commit=False)
                add_listing.user = request.user
                add_listing.save()

                # loop through job skills and insert into database
                for skill in request.session['job_skills']:
                    JobSkill.objects.create(skill_id=skill[0], skill_name=skill[1], job_id=add_listing.id)

                # delete session holding the job skills
                del request.session['job_skills']

                return redirect('job_listings')
            else:
                return render(request, 'add_joblisting.html', {'form': form})
        else:
            form = NewJobListingForm()
        return render(request, 'add_joblisting.html', {'form': form})
    except ObjectDoesNotExist:
        return redirect('restricted_access')


@login_required
def recruiter_profile(request):
    user_id = request.user.id
    try:
        # Prefetch related PersonalInformation data
        saved_users_with_info = SavedUsers.objects.filter(recruiter=request.user).prefetch_related(
            'saved__personal_information')

        personal_info = PersonalInformation.objects.get(user=request.user)
        messages = user_list_messages(request)
        job_listings = JobListing.objects.filter(user_id=user_id)

        jobs_filter = AppliedJobs.objects.select_related('user_id').filter(job__in=job_listings)
        applied_jobs = jobs_filter.values('job_id', 'user_id', 'user_id__first_name', 'user_id__last_name',
                                          'job__title', 'job__company', 'cover_letter')

        context = {'pii': personal_info,
                   'jobs': job_listings,
                   'applied': applied_jobs,
                   'users': saved_users_with_info,
                   'messages': messages}

        # Check if job_listings is empty
        # todo: change this to show to the user on profile page
        if not job_listings:
            print("No job listings found for user:", user_id)

    except PersonalInformation.DoesNotExist:
        return redirect('add_personalinfo')

    return render(request, 'recruiter_profile.html', context)


@login_required
def job_listings(request):
    user_id = request.user.id

    personal_info = PersonalInformation.objects.get(user=request.user)
    job_listings = JobListing.objects.filter(user_id=user_id)

    context = {'pii': personal_info, 'jobs': job_listings}

    return render(request, 'recruiters/all_jobs.html', context)


def user_applications(request):
    user_id = request.user.id
    try:
        personal_info = PersonalInformation.objects.get(user=request.user)
        job_listings = JobListing.objects.filter(user_id=user_id)

        jobs_filter = AppliedJobs.objects.select_related('user_id').filter(job__in=job_listings)
        applied_jobs = jobs_filter.values('job_id', 'user_id', 'user_id__first_name', 'user_id__last_name',
                                          'job__title', 'job__company', 'cover_letter')

        context = {'pii': personal_info,
                   'applied': applied_jobs}

        # Check if job_listings is empty
        # todo: change this to show to the user on profile page
        if not job_listings:
            print("No job listings found for user:", user_id)

    except PersonalInformation.DoesNotExist:
        return redirect('add_personalinfo')

    return render(request, 'recruiters/applications.html', context)


@login_required
def saved_resumes(request):
    # Prefetch related PersonalInformation data
    saved_users_with_info = SavedUsers.objects.filter(recruiter=request.user).prefetch_related(
        'saved__personal_information')

    personal_info = PersonalInformation.objects.get(user=request.user)

    context = {'pii': personal_info, 'users': saved_users_with_info}

    return render(request, 'recruiters/saved_resumes.html', context)


def job_skill_add(request):
    context = {}
    if request.method == 'POST':
        form = JobSkillForm(request.POST)
        if form.is_valid():
            job_skill = form.save(commit=False)
            job_skill.user = request.user
            job_skill.skill_id = 8
            job_skill.save()
            context['skill'] = job_skill
            return render(request, 'skill_col.html', context)
        else:
            print('form is invalid')
    else:
        form = JobSkillForm()
    context['form'] = form
    return render(request, 'add_job_skill.html', context)
