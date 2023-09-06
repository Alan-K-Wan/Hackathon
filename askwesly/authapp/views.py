# authapp/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os
import openai

@login_required
def secret_page(request):
    # Access the user's name
    user_name = request.user.username

    # Pass the user's name to the template
    context = {'user_name': user_name}
    return render(request, 'authapp/secret_page.html', context)

@login_required
def process_input(request):

    prompt = '''
    Can you respond with the following context/requirements to all further messages that you get
    - you are to respond professionally, friendly like a service desk technician
    - the response needs to be succinct (try to respond with 2 sentences or less)
    - you need to get as much information regarding the request as possible
    - if the request doesn't make any sense then politely reply asking for clarification
    - Ask the user for relevant information in relation to the request but not questions that will not help them solve their problem
    - Don't overbear the user with questions (Only  1 question at a time)
    - Where possible try to link the user to relevant self help article
    - If linking to a self help article, follow through by asking if it helped or not
    - identify the impact by asking if its just them or do they know others who are also affected
    - wrap any links in html anchor tags and make them open in a new tab
    '''

    openai.api_key = os.environ.get('OPENAI_API_KEY')

    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')

        # Create a list of message dictionaries in the OpenAI format
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text}
        ]

        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=75
        )

        reply = chat.choices[0].message.content

        # Append the assistant's reply to the messages
        messages.append({"role": "assistant", "content": reply})

        # Process the input (you can replace this with your actual processing logic)
        processed_output = reply

        # Return the processed result as JSON
        return JsonResponse({'result': processed_output})

    return JsonResponse({'error': 'Invalid request method'})

    


