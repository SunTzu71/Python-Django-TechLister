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
    form = AddEducationForm(request.POST)
    context['form'] = form
    if form.is_valid():
        add_education = form.save(commit=False)
        add_education.user = request.user
        add_education.save()

        context['education'] = add_education
        return render(request, 'education_row.html', context)
    else:
        return render(request, 'ai_add_education.html', context)
    return render(request, 'education_row.htnl', context)


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
    if request.method == 'POST':
        form = AddEducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return render(request, 'education_row.html', context)
        else:
            return render(request, 'ai_edit_education.html', context)
    else:
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


def ai_add_experience(request):
    form = AddExperienceForm(request.POST)
    return render(request, 'ai_add_experience.html', {'form': form})


def add_experience_submit(request):
    print('add experience submit')
    context = {}
    form = AddExperienceForm(request.POST)
    context['form'] = form
    if form.is_valid():
        print('form is valid')
        add_experience = form.save(commit=False)
        add_experience.user = request.user
        add_experience.save()

        context['experience'] = add_experience
        return render(request, 'experience_row.html', context)
    else:
        print('form is invalid')
        return render(request, 'ai_add_experience.html', context)
    return render(request, 'experience_row.htnl', context)
