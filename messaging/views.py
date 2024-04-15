from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import MessageForm


@login_required
def new_message(request, to_user_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            add_message = form.save(commit=False)
            add_message.from_user = request.user
            add_message.to_user = User.objects.get(pk=to_user_id)
            add_message.save()
            return render(request, 'messages/message-sent.html')
        else:
            return render(request, 'new_message.html', {'form': form})
    else:
        print('not posting')
        form = MessageForm()
    return render(request, 'new_message.html', {'form': form})
