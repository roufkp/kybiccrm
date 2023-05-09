# from django.shortcuts import render
# # Create your views here.
# from twilio.rest import Client
# import openai 
# import os
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from twilio.twiml.messaging_response import MessagingResponse

# # Set up Twilio client
# account_sid = 'AC7ceee1e881b956cfad4c29a4a6728439'
# auth_token = '03e85dbe2d59e9555d8e9b8725fc29f0'
# client = Client(account_sid, auth_token)

# # Set up ChatGPT API
# openai.api_key = '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'

# @csrf_exempt
# def handle_message(request):
#     # Get the incoming message and sender
#     incoming_message = request.POST.get('Body', '')
#     sender = request.POST.get('From', '')

#     # Generate a response using ChatGPT
#     prompt = f"User: {incoming_message}\nAI:"
#     response = openai.Completion.create(
#         engine='ada',
#         prompt=prompt,
#         max_tokens=500
#     )
#     outgoing_message = response.choices[0].text.strip()

#     # Send the response back to the user using Twilio
#     twilio_response = MessagingResponse()
#     twilio_response.message(outgoing_message)
#     return HttpResponse(str(outgoing_message,))



################## using webhook############################

from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from django.http import HttpResponse

# Set up ChatGPT API
openai.api_key = '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'

# Define function to generate response from ChatGPT API
def generate_response(message):
    prompt = f"User: {message}\nAI:"
    response = openai.Completion.create(
        engine='ada',
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

# Define view function to handle incoming messages
def whatsapp_callback(request):
    if request.method == 'POST':
        # Get the incoming message and sender's phone number
        message = request.POST.get('Body', '')
        sender = request.POST.get('From', '').split(':')[1]

        # Generate a response using ChatGPT
        response = generate_response(message)

        # Send the response back to the user
        twilio_response = MessagingResponse()
        twilio_response.message(response)
        return HttpResponse(str(twilio_response))
    else:
        return HttpResponse(status=405)
