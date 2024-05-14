from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import render, redirect
from website.models import SavedJobs, AppliedJobs, PersonalInformation, Education, Experience, UserSkill, AIToken
from messaging.views import user_list_messages
from website.views import get_resume_information


@login_required
def user_profile(request):
    try:
        personal_info = PersonalInformation.objects.get(user_id=request.user.id)
        messages = user_list_messages(request)
        context = {'pii': personal_info, 'messages': messages}

    except PersonalInformation.DoesNotExist:
        return redirect('add_personalinfo')

    # check if user or recruiter and redirect to profile page
    if personal_info.recruiter:
        return render(request, 'recruiter_profile.html',  context)
    else:
        return render(request, 'user_profile.html',  context)


@login_required
def saved_jobs(request):
    user_id = request.user.id
    try:
        saved_jobs = SavedJobs.objects.filter(user_id=user_id).select_related('job')
    except SavedJobs.DoesNotExist:
        saved_jobs = None

    try:
        personal_info = PersonalInformation.objects.get(user_id=user_id)
    except PersonalInformation.DoesNotExist:
        return redirect('add_personal_info')

    if not saved_jobs or not personal_info:
        return redirect('user_profile')

    context = {'saved_jobs': saved_jobs, 'pii': personal_info}
    return render(request, 'users/saved_jobs.html', context)


@login_required
def applied_jobs(request):
    try:
        user_id = request.user.id
        applied_jobs = AppliedJobs.objects.filter(user_id=user_id).select_related('job')
        try:
            personal_info = PersonalInformation.objects.get(user_id=user_id)
        except PersonalInformation.DoesNotExist:
            return redirect('add_personal_info')

        context = {'applied_jobs': applied_jobs, 'pii': personal_info}
    except SavedJobs.DoesNotExist:
        return redirect('user_profile')
    return render(request, 'users/applied_jobs.html', context)


@login_required
def edit_resume(request):
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

    return render(request, 'users/edit_resume.html', context)


from django.shortcuts import get_object_or_404


@login_required
def ai_info(request):
    user_id = request.user.id
    personal_info = get_object_or_404(PersonalInformation, user_id=user_id)
    ai_token = get_object_or_404(AIToken, user=request.user)
    context = {'pii': personal_info,
               'ai_token': ai_token}
    return render(request, 'users/ai_info.html', context)
