from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Message
from django.contrib.auth.decorators import login_required
from .forms import SendMessageForm
from datetime import datetime

# Create your views here.
@login_required
def index(request):
    try:
        inbox = Message.objects.filter(recipient=request.user)[:10]
        outbox = Message.objects.filter(sender=request.user)[:10]
    except:
        inbox = None
        outbox= None

    return render(request, 'message_index.html', {'inbox': inbox, 'outbox': outbox})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = SendMessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.time = datetime.now()
            message.sender = request.user
            message.is_opened = False
            message.save()
            return redirect('/messages/')

    else:
        form = SendMessageForm()

    return render(request, 'send_message.html', {'form': form})

@login_required
def view_message(request, msg_id):
    message = get_object_or_404(Message, pk=msg_id)
    message.is_opened = True
    message.save()
    return render(request, 'message_view.html', {'message': message})

@login_required
def view_inbox(request):
    inbox = get_list_or_404(Message, recipient=request.user)
    return render(request, 'inbox.html', {'inbox':inbox})