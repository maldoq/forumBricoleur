# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Add this import at the top
from django.http import JsonResponse
from .models import MessageChat, Chat
from auths.models import User

@login_required
def conversations_view(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, idUser=user_id)

    # Get all chats where the user is either user1 or user2
    chats = Chat.objects.filter(
        Q(user1=user) | Q(user2=user)
    ).select_related('user1', 'user2').order_by('-dateModif')

    # Transform chats to show the other user in each chat
    other_chats = []
    for chat in chats:
        other_user = chat.user2 if chat.user1 == user else chat.user1
        other_chats.append({
            'chat': chat,
            'other_user': other_user
        })

    chat_id = request.GET.get('chat_id')
    active_chat_instance = None
    messages = []
    
    if chat_id:
        active_chat_instance = get_object_or_404(
            Chat.objects.select_related('user1', 'user2'),
            idChat=chat_id,
        )
        messages = MessageChat.objects.filter(
            chat=active_chat_instance
        ).select_related('user').order_by('dateAdd')

    # Get available users for new chats
    existing_chat_users = Chat.objects.filter(
        Q(user1=user) | Q(user2=user)
    ).values_list('user1', 'user2')
    
    # Flatten and remove duplicates
    chatting_with = set()
    for u1, u2 in existing_chat_users:
        chatting_with.add(u1)
        chatting_with.add(u2)
    
    available_users = User.objects.exclude(
        idUser__in=chatting_with
    ).exclude(
        idUser=user.idUser
    )

    return render(request, 'contain/chat.html', {
        'other_chats': other_chats,
        'active_chat_instance': active_chat_instance,
        'messages': messages,
        'available_users': available_users,
        'current_user': user,  # Add current user to context
    })

@login_required
def send_message_view(request, chat_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, idUser=user_id)
    
    chat_instance = get_object_or_404(
        Chat,
        idChat=chat_id,
    )

    message_content = request.POST.get('message')
    if not message_content:
        return JsonResponse({'error': 'Message cannot be empty'}, status=400)

    message = MessageChat.objects.create(
        chat=chat_instance,
        user=user,
        descriptMes=message_content,
    )
    
    # Update chat's dateModif
    chat_instance.save()  # This will update dateModif due to auto_now=True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': {
                'id': message.idMes,
                'content': message.descriptMes,
                'user': user.pseudoUser,
                'timestamp': message.dateAdd.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    
    return redirect('conversations')

@login_required
def create_chat_view(request, user_id):
    current_user_id = request.session.get('user_id')
    current_user = get_object_or_404(User, idUser=current_user_id)
    other_user = get_object_or_404(User, idUser=user_id)

    # Prevent creating chat with self
    if current_user == other_user:
        return JsonResponse({'error': 'Cannot create chat with yourself'}, status=400)

    # Check if chat exists in either direction
    existing_chat = Chat.objects.filter(
        Q(user1=current_user, user2=other_user) |
        Q(user1=other_user, user2=current_user)
    ).first()

    if not existing_chat:
        existing_chat = Chat.objects.create(
            user1=current_user,
            user2=other_user
        )

    return redirect(f'/chat/conversations/?chat_id={existing_chat.idChat}')