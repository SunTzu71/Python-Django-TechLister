from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import MessageForm


@login_required
def new_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            add_message = form.save(commit=False)
            add_message.from_user = request.user
            add_message.to_user = 8
            add_message.save()
            return redirect('user_profile')
        else:
            return render(request, 'new_message.html', {'form': form})
    else:
        form = MessageForm()
    return render(request, 'new_message.html', {'form': form})
