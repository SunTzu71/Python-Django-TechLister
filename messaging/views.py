from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import MessageForm, ReplyMessageForm
from .models import Message, MessageReply
from website.models import PersonalInformation


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
            check_user = Message.objects.get(Q(to_user=request.user) | Q(from_user=request.user), id=msg_id)

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
        from_user_messages = Message.objects.filter(from_user=user_instance)
        to_user_messages = Message.objects.filter(to_user=user_instance)
        all_messages = from_user_messages.union(to_user_messages).order_by('read')
        return all_messages
    except Message.DoesNotExist:
        return redirect('user_profile')


@login_required
def view_message(request, msg_id):
    try:
        personal_info = PersonalInformation.objects.get(user=request.user)

        message = Message.objects.get(Q(to_user=request.user) | Q(from_user=request.user), pk=msg_id)
        message.read = True
        message.save()

        replies = MessageReply.objects.filter(message_id=message.id)
        for reply in replies:
            reply.read = True
            reply.save()

        context = {'message': message,
                   'pii': personal_info,
                   'replies': replies,
                   'msg_id': msg_id}

        return render(request, 'messages/view-message.html', context)
    except Message.DoesNotExist:
        return redirect('user_profile')


@login_required
def delete_message(request, msg_id):
    try:
        delete_message = Message.objects.get(Q(to_user=request.user) | Q(from_user=request.user), pk=msg_id)
        delete_message.delete()
        return HttpResponse('')
    except Message.DoesNotExist:
        return redirect('home')
