from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

from website.models import PersonalInformation, Education, Experience, UserSkill
from website.forms import AddEducationForm


# Create your views here.
@login_required
def ai_resume(request):
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

    return render(request, 'ai_resume.html', context)


@login_required
def ai_edit_education(request, pk):
    try:
        education = Education.objects.get(user=request.user, pk=pk)
        form = AddEducationForm(instance=education)
        context = {'form': form, 'edu_id': pk}

        if request.method == 'POST':
            form = AddEducationForm(request.POST, instance=education)
            if form.is_valid():
                form.save()
                edu_context  = {'edu': education}
                return render(request, 'education_snippet.html', edu_context)
        else:
            return render(request, 'ai_edit_education.html', context)
    except ObjectDoesNotExist:
        return redirect('restricted_access')
