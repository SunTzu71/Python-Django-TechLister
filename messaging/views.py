from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import MessageForm, ReplyMessageForm
from .models import Message, MessageReply


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
            return render(request, 'new_message.html', context)
    else:
        form = MessageForm()
        context = {'form': form, 'user_id': user_id}
    return render(request, 'new_message.html', context)


@login_required
def reply_message(request, msg_id, user_id):
    if request.method == 'POST':
        try:
            # check if user has access to reply
            check_user = Message.objects.get(id=msg_id, to_user=request.user)

            form = ReplyMessageForm(request.POST)
            context = {'form': form, 'msg_id': msg_id, 'user_id': user_id}

            if form.is_valid():
                # set main message to read False to show new message alert
                main_read = Message.objects.get(id=msg_id)
                main_read.read = False
                main_read.save()

                add_message = form.save(commit=False)
                add_message.from_user = request.user
                add_message.to_user = User.objects.get(pk=user_id)
                add_message.message_id = msg_id
                add_message.save()

                return render(request, 'messages/message-sent.html')
            else:
                return render(request, 'reply_message.html', context)
        except Message.DoesNotExist:
            # Handle the case where the user in request.user is not in the to_user of Message
            return redirect('restricted_access')
    else:
        form = ReplyMessageForm()
        context = {'form': form, 'msg_id': msg_id, 'user_id': user_id}
    return render(request, 'reply_message.html', context)


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
        message.read = True
        message.save()

        # we do not need this logic
        replies = MessageReply.objects.filter(message_id=message.id)
        for reply in replies:
            reply.read = True
            reply.save()

        context = {'message': message,
                   'replies': replies,
                   'msg_id': msg_id}

        return render(request, 'messages/view-message.html', context)
    except Message.DoesNotExist:
        return redirect('user_profile')


@login_required
def delete_message(request, msg_id):
    try:
        delete_message = Message.objects.get(to_user=request.user, pk=msg_id)
        delete_message.delete()
        return HttpResponse('')
    except Message.DoesNotExist:
        return redirect('user_profile')
