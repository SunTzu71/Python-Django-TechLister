from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

from website.models import PersonalInformation, Education, Experience, UserSkill
from website.forms import AddEducationForm, AddExperienceForm


# Create your views here.
@login_required
def ai_resume(request):
    return render(request, 'ai_resume.html')


def get_skill_list(request):
    user_skills = UserSkill.objects.filter(user=request.user)
    context = {'uskills': user_skills}
    return render(request, 'skill_list.html', context)


def ai_skill_delete(request, skill_id):
    skill = UserSkill.objects.get(pk=skill_id)
    skill.delete()
    return HttpResponse()

def get_education_list(request):
    user_id = request.user.id
    education_info = Education.objects.filter(user_id=user_id)
    context = {'education_info': education_info}
    return render(request, 'education_list.html', context)


def ai_add_education(request):
    form = AddEducationForm(request.POST)
    return render(request, 'ai_add_education.html', {'form': form})


def add_education_submit(request):
    context = {}
    if request.method == 'POST':
        form = AddEducationForm(request.POST)
        if form.is_valid():
            add_education = form.save(commit=False)
            add_education.user = request.user
            add_education.save()
            context['education'] = add_education
            return render(request, 'education_row.html', context)
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = AddEducationForm()
    context['form'] = form
    return render(request, 'ai_add_education.html', context)


def add_education_cancel(request):
    return HttpResponse('')


def ai_edit_education(request, pk):
    education = Education.objects.get(user=request.user, pk=pk)
    context = {}
    context['education'] = education
    context['form'] = AddEducationForm(initial={
        'title': education.title,
        'description': education.description,
    })
    return render(request, 'ai_edit_education.html', context)


@login_required
def edit_education_submit(request, pk):
    context = {}
    education = Education.objects.get(user=request.user, pk=pk)
    context['education'] = education

    context['form'] = AddEducationForm(initial={
        'title': education.title,
        'description': education.description,
    })

    if request.method == 'POST':
        form = AddEducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            context['education'] = education
            return render(request, 'education_row.html', context)
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = AddEducationForm(instance=education)
    context['form'] = form
    return render(request, 'education_row.html')


def edit_education_cancel(request, pk):
    context = {}
    education = Education.objects.get(user=request.user, pk=pk)
    context['education'] = education
    return render(request, 'education_row.html', context)


def delete_education(request, pk):
    education = Education.objects.get(pk=pk)
    education.delete()
    return HttpResponse()


def get_experience_list(request):
    user_id = request.user.id
    experience_info = Experience.objects.filter(user_id=user_id)
    context = {'experience_info': experience_info}
    return render(request, 'experience_list.html', context)


def add_experience_submit(request):
    context = {}
    if request.method == 'POST':
        form = AddExperienceForm(request.POST)
        if form.is_valid():
            add_experience = form.save(commit=False)
            add_experience.user = request.user
            add_experience.save()
            context['experience'] = add_experience
            return render(request, 'experience_row.html', context)
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = AddExperienceForm()
    context['form'] = form
    return render(request, 'ai_add_experience.html', context)


def add_experience_cancel(request):
    return HttpResponse('')


def ai_delete_experience(request, pk):
    experience = Experience.objects.get(pk=pk)
    experience.delete()
    return HttpResponse()


@login_required
def edit_experience_submit(request, pk):
    context = {}
    experience = Experience.objects.get(user=request.user, pk=pk)
    context['experience'] = experience

    context['form'] = AddExperienceForm(initial={
        'company': experience.company,
        'position': experience.position,
        'start_month': experience.start_month,
        'start_year': experience.start_year,
        'end_month': experience.end_month,
        'end_year': experience.end_year,
        'currently_working': experience.currently_working,
        'task_one': experience.task_one,
        'task_two': experience.task_two,
        'task_three': experience.task_three,
        'task_four': experience.task_four,
        'task_five': experience.task_five,
        'task_six': experience.task_six,
        'task_seven': experience.task_seven,
        'task_eight': experience.task_eight,
        'task_nine': experience.task_nine,
        'task_ten': experience.task_ten,
    })

    if request.method == 'POST':
        form = AddExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            context['experience'] = experience
            return render(request, 'experience_row.html', context)
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = AddExperienceForm(instance=experience)
    context['form'] = form
    return render(request, 'ai_edit_experience.html', context)


def edit_experience_cancel(request, pk):
    context = {}
    experience = Experience.objects.get(user=request.user, pk=pk)
    context['experience'] = experience
    return render(request, 'experience_row.html', context)
