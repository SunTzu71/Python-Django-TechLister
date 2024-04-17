from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from website.models import SavedUsers, PersonalInformation, JobListing, AppliedJobs
from messaging.views import user_list_messages

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


@login_required
def saved_resumes(request):
    # Prefetch related PersonalInformation data
    saved_users_with_info = SavedUsers.objects.filter(recruiter=request.user).prefetch_related(
        'saved__personal_information')

    personal_info = PersonalInformation.objects.get(user=request.user)

    context = {'pii': personal_info, 'users': saved_users_with_info}

    return render(request, 'recruiters/saved_resumes.html', context)
