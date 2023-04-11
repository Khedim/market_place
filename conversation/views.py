from django.shortcuts import redirect, render, get_object_or_404
from items.models import Item
from .models import Conversation
from .forms import ConversationMessgesForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if request.user == item.created_by:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessgesForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(item.created_by)
            conversation.members.add(request.user)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)

    else :
        form = ConversationMessgesForm()

    context = {
        'form': form
    }

    return render(request, 'conversation/new.html', context)

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessgesForm(request.POST)
        if form.is_valid():

                conversation_message = form.save(commit=False)
                conversation_message.conversation = conversation
                conversation_message.created_by = request.user
                conversation_message.save()

                conversation.save()

                return redirect('conversation:detail', pk=pk)
    
    else :
        form = ConversationMessgesForm()

    return render(request, 'conversation/detail.html', {
        'form': form,
        'conversation': conversation
    })
 