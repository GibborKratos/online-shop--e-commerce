from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q, F
from django.utils.safestring import mark_safe
import json

from .models import Message
from accounts.models import CustomUser

@login_required
def index(request):
    unique_interactions = []
    interaction_data = {}
    
    for message in Message.objects.filter(Q(author=request.user) | Q(recipient=request.user)):
        interaction_data = {}
        other_user_id = None
        other_user_name = None
        
        if message.author == request.user:
            other_user_id = message.recipient_id
            other_user = CustomUser.objects.get(pk=other_user_id)
            interaction_data['author_username'] = request.user.username
            interaction_data['recipient_username'] = other_user.username
        else:
            other_user_id = message.author_id
            other_user = CustomUser.objects.get(pk=other_user_id)
            interaction_data['author_username'] = other_user.username
            interaction_data['recipient_username'] = request.user.username
        
            # Lookup the username for the other_user_id
        try:
            other_user = CustomUser.objects.get(pk=other_user_id)
            other_user_name = f"{other_user.first_name} {other_user.last_name}"
            interaction_data['other_user_name'] = other_user_name
            print(f"Other_user_name: {other_user_name}")
        except CustomUser.DoesNotExist:
            print(f"No user found for ID: {other_user_id}")
            continue  # Skip to the next iteration if no user is found
    
    

    # Ensure this interaction doesn't already exist in unique_interactions
    if not any(interaction['recipient_id'] == interaction_data['recipient_id'] and 
               interaction['author_id'] == interaction_data['author_id'] for interaction in unique_interactions):
        unique_interactions.append(interaction_data)

        print(f"Recipient : {request.GET.get('recipient')} author: {request.GET.get('author')}")

        filtered_interactions = [interaction for interaction in unique_interactions if interaction.get('recipient_username') or interaction.get('author_username')]

    
        
    return render(request, "chat/room.html", {
        "room_name": mark_safe(json.dumps("room")),
        "author": mark_safe(json.dumps(request.GET.get("author"))),
        "recipient": mark_safe(json.dumps(request.GET.get("recipient"))),
        "unique_interactions" : filtered_interactions,
    })
