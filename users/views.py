from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.cache import cache
from django.template.loader import render_to_string
from django.conf import settings
from openai import OpenAI

from website.models import PersonalInformation, Education, Experience, UserSkill, User, AIToken
from website.forms import (AddEducationForm, AddExperienceForm, UserSkillForm, PersonalInformationForm,
                           AIPersonalAboutForm)


def get_about_info(user_inst):
    pii = PersonalInformation.objects.get(user=user_inst)
    return pii


def get_ai_experience(user_inst):
    exp = Experience.objects.filter(user=user_inst)
    return exp


@login_required
def ai_resume(request):
    # get token amount to display AI button
    user_tokens = AIToken.objects.filter(user=request.user).first()
    if user_tokens is None:
        ai_token = AIToken(user=request.user, amount=0)
        ai_token = False
    else:
        ai_token = True

    context = {
        'pii': get_about_info(request.user),
        'exps': get_ai_experience(request.user),
        'ai_token': ai_token,
    }
    return render(request, 'ai_resume.html', context)


def get_skill_list(request):
    user_skills = UserSkill.objects.filter(user=request.user)
    context = {'uskills': user_skills}
    return render(request, 'skill_list.html', context)


@login_required
def ai_skill_add(request):
    context = {}
    if request.method == 'POST':
        form = UserSkillForm(request.POST)
        if form.is_valid():
            user_skill = form.save(commit=False)
            user_skill.user = request.user
            user_skill.save()
            context['skill'] = user_skill
            return render(request, 'skill_col.html', context)
        else:
            print('form is invalid')
    else:
        form = UserSkillForm()
    context['form'] = form
    return render(request, 'add_user_skill.html', context)


def add_skill_cancel(request):
    return HttpResponse('')


@login_required
def ai_skill_delete(request, skill_id):
    skill = UserSkill.objects.get(pk=skill_id)
    skill.delete()
    return HttpResponse()


@login_required
def get_education_list(request):
    user_id = request.user.id
    education_info = Education.objects.filter(user_id=user_id)
    context = {'education_info': education_info}
    return render(request, 'education_list.html', context)


@login_required
def ai_add_education(request):
    form = AddEducationForm(request.POST)
    return render(request, 'ai_add_education.html', {'form': form})


@login_required
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


@login_required
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


@login_required
def delete_education(request, pk):
    education = Education.objects.get(pk=pk)
    education.delete()
    return HttpResponse()


def get_experience_list(request):
    user_id = request.user.id
    experience_info = Experience.objects.filter(user_id=user_id)
    context = {'experience_info': experience_info}
    return render(request, 'experience_list.html', context)


@login_required
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


@login_required
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


def generate_about(user_id):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    user_instance = get_object_or_404(User, id=user_id)
    user_about = get_about_info(user_instance)
    prompt = (f"Write me a about section that is no longer than 5 sentences. "
              f"Then paste the about into the input text.\n\nJob Description:\n{user_about.about}\n\nAbout:")

    # Use the new ChatCompletion of OpenAI to generate the cover letter
    response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])

    # Get the generated cover letter from the response
    about_section = response.choices[0].message.content.strip()

    user_tokens = AIToken.objects.get(user=user_instance)
    if user_tokens.amount > 0:
        user_tokens.amount = user_tokens.amount - 1
        user_tokens.save()

    return about_section


@login_required
def ai_about_me(request):
    gen_about = generate_about(request.user.id)
    personal_info = PersonalInformation.objects.get(user=request.user)
    form = AIPersonalAboutForm(request.POST or None, instance=personal_info,
                               initial={'about': gen_about})

    context = {'form': form}
    return render(request, 'ai_about_me.html', context)


@login_required
def ai_about_update(request):
    personal_info = PersonalInformation.objects.get(user=request.user)
    if request.method == 'POST':
        form = AIPersonalAboutForm(request.POST, instance=personal_info)
        if form.is_valid():
            ai_about = form.save(commit=True)
            return redirect('ai_resume')


def generate_exp_tasks(user_id, exp_id):
    experience = Experience.objects.get(id=exp_id)
    task_fields = ['task_one', 'task_two', 'task_three', 'task_four', 'task_five',
                   'task_six', 'task_seven', 'task_eight', 'task_nine', 'task_ten']
    tasks = [getattr(experience, field) for field in task_fields]
    task_list = ""
    for task in tasks:
        if task:
            task_list += f"{task}"
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = (f"Go through the list of tasks updating the description to be more appealing. "
              f"Do not duplicate the task_list in the response "
              f"Then paste the numbered list into the input text.{task_list}")

    response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
                                              messages=[
                                                  {"role": "system", "content": "You are a helpful assistant."},
                                                  {"role": "user", "content": prompt}
                                              ])
    # Get the generated tasks from the response
    new_tasks = response.choices[0].message.content.strip()

    user_instance = get_object_or_404(User, id=user_id)
    user_tokens = AIToken.objects.get(user=user_instance)
    if user_tokens.amount > 0:
        user_tokens.amount = user_tokens.amount - 1
        user_tokens.save()

    return new_tasks


@login_required
def ai_experience_update(request, exp_id):
    experience = Experience.objects.get(id=exp_id)
    task_fields = ['task_one', 'task_two', 'task_three', 'task_four', 'task_five',
                   'task_six', 'task_seven', 'task_eight', 'task_nine', 'task_ten']

    get_cache_name = f'gen_tasks_{exp_id}'
    tasks = cache.get(get_cache_name, [])

    for task, field in zip(tasks, task_fields):
        task = task.split('. ', 1)[-1]  # Strip out the part before ". "
        setattr(experience, field, task)

    experience.save()

    return redirect('ai_resume')


@login_required
def ai_experience_tasks(request):
    if request.method == 'POST':
        exp_id = request.POST.get('exp_id')
        experience = Experience.objects.get(id=exp_id)
        task_fields = ['task_one', 'task_two', 'task_three', 'task_four', 'task_five',
                       'task_six', 'task_seven', 'task_eight', 'task_nine', 'task_ten']

        gen_tasks = generate_exp_tasks(request.user.id, exp_id)
        task_list = gen_tasks.split('\n')

        # Store the tasks in cache
        cache_name = f'gen_tasks_{exp_id}'
        cache.set(cache_name, task_list, 300)  # Cache data for 5 minutes

        context = {'exp_id': exp_id, 'tasks': task_list}

        return render(request, 'ai_experience_tasks.html', context)
