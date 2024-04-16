from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import MessageForm
from .models import Message


@login_required
def new_message(request, user_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        context = {'form': form, 'user_id': user_id}
        if form.is_valid():
            add_message = form.save(commit=False)
            add_message.from_user = request.user
            add_message.to_user = User.objects.get(pk=user_id)
            add_message.save()
            return render(request, 'messages/message-sent.html')
        else:
            return render(request, 'new_message.html', {context})
    else:
        form = MessageForm()
        context = {'form': form, 'user_id': user_id}
    return render(request, 'new_message.html', context)


@login_required
def user_list_messages(request):
    try:
        user_instance = request.user
        all_messages = user_instance.to_messages.all()
        return all_messages
    except Message.DoesNotExist:
        return redirect('user_profile')


@login_required
def view_message(request, msg_id):
    try:
        message = Message.objects.get(to_user=request.user, pk=msg_id)
        context = {'message': message, 'msg_id': msg_id}
        return render(request, 'messages/view-message.html', context)
    except Message.DoesNotExist:
        return redirect('user_profile')


@login_required
def delete_message(request, msg_id):
    try:
        delete_message = Message.objects.get(to_user=request.user, pk=msg_id)
        delete_message.delete()
        return HttpResponse('<script>document.querySelector("#message-row-' + str(id) + '").remove()</script>')
    except Message.DoesNotExist:
        return redirect('user_profile')
