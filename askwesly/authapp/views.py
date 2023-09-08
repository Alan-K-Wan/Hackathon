# authapp/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os
import openai
from django.contrib.auth.models import User
from .models import UserProfile
import json
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_PASSWORD = 'nnfjtvhcampxisou'

prompt = '''
    Can you respond with the following context/requirements to all further messages that you get
    - you are to respond professionally and friendly like a service desk technician
    - the response needs to be succinct (try to respond with 2 sentences or less)
    - you need to get as much information regarding the request as possible
    - if the request doesn't make any sense then politely reply asking for clarification
    - Ask the user for relevant information in relation to the request but not questions that will not help them solve their problem
    - Don't overbear the user with questions (Only  1 question at a time)
    - Where possible try to link the user to relevant self help article
    - If there is a clear article to link to then don't bother asking extra questions
    - If linking to a self help article then follow through by asking if it helped or not
    - identify the impact by asking if its just them or do they know others who are also affected
    - Always wrap any website links in html anchor tags and make them open in a new tab
    - Do not ever respond with "I don't know" or "I can't help you"
    - If it is a request that cannot be fulfilled by linking to a self helf article (for example borrowing a laptop) then gather enough information to craft an email that can be sent to the relevant team
    - If the request cannot be completed by simply linking to an article then clearly state that you (the assistant) will subnit a ticket on the clients behalf
    - Remember that it is preferred that a ticket is submitted rather than the client getting annoyed and clicking off the page
    - There is no need to ask for contact information as this is already provided by the user's profile
    - Once you have gathered enough information to submit a ticket then clearly state that you will submit a ticket on the clients behalf
    - Always submit a ticket if the user is reprting something serious like a cyber incident, safety hazard, large scale outage, etc.
    - Do not say anything that you don't know is completely true. If you don't know then say something like "the it Team will investigate and get back to you"
    - Remember to always say you will submit a ticket on the clients behalf if they are reporting something that requires IT attention
    - Always ask the user if they are okay with you (the ai assistant) submitting a ticket on their behalf. If they say yes then confirm that you have. If they say no then confirm that you will not. This is very important
    - If the user would like to inform IT of something for example a cyber incident (no matter the severity) then gather the required information and submit a ticket on the clients behalf
    - If the a user is reporting something that doesn't require IT attention then ALWAYS ask if they would like to submit a ticket anyway
    - If the user is concerned about submitting a ticket then assure them that it is the best way to get their issue resolved and ask them again if they want to submit a ticket. 
    - If the user wants to reset a password always ask which account they want to reset before providing a link to a guide to reset it themselves if there is one
    - If the user is requesting a service from IT then ask them to provide information about the service and submit a ticket on their behalf
    - it is imperetive that you ask the user if they are okay with a ticket being submitted.
    '''

default = {
            'msg': [{"role": "system", "content": prompt}]
          }

ticket_submitted = '''
    Respond "TRUE" to my next message only if the following conditions are met
    - the message is confirming that a ticket has been submitted or an email has been sent to the service desk.
    - it doesn't count if the message is asking for confirmation to submit a ticket
    - There are no pending information that is still required
    - The message doesn't ask something like "are you okay with this"
    Otherwise respond "FALSE". ONLY respond with one word "TRUE" or "FALSE" to the next message
    '''

approval = [{
    'msg': {"role": "system", "content": ticket_submitted}
}]

@login_required
def secret_page(request):
    # Access the user's name
    user_name = request.user.username

    # get list of message dictionaries in Open AI format from DB
    user = User.objects.get(username=user_name)

    # set text_field to default every time the user gets taken to secret page
    if not hasattr(user, 'userprofile'):
        user_profile = UserProfile.objects.create(user=user, text_field=json.dumps(default))
    else:
        user_profile = UserProfile.objects.get(user=user)
        user_profile.text_field = json.dumps(default)
        user_profile.save()

    # Pass the user's name to the template
    context = {'user_name': user_name}
    return render(request, 'authapp/secret_page.html', context)
    

@login_required
def process_input(request):

    openai.api_key = os.environ.get('OPENAI_API_KEY')

    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')

        # get list of message dictionaries in Open AI format from DB
        user = User.objects.get(username=request.user.username)

        # set text_field to default if it doesn't exist
        if not hasattr(user, 'userprofile'):
            user_profile = UserProfile.objects.create(user=user, text_field=json.dumps(default))

        user_profile = UserProfile.objects.get(user=user)

        # convert text_field to a list of dictionaries
        data = json.loads(user_profile.text_field)

        # get msg from data and store it in a variable called temp
        listdict = data['msg']

        messages = listdict

        # Append the user's input to the messages
        messages.append({"role": "user", "content": input_text})

        chat = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=150
        )

        reply = chat.choices[0].message.content

        # Append the assistant's reply to the messages
        messages.append({"role": "system", "content": reply})

        # Save the messages to the database
        data['msg'] = messages
        user_profile.text_field = json.dumps(data)
        user_profile.save()

        # Process the input (you can replace this with your actual processing logic)
        processed_output = reply

        # Send an email if the user confirms that they want the ticket submitted

        approval = [
            {"role": "system", "content": ticket_submitted}
        ]

        approval.append({"role": "user", "content": processed_output})

        check_approved = openai.ChatCompletion.create(
            model="gpt-4",
            messages=approval,
            max_tokens=150
        )

        trueFalse = check_approved.choices[0].message.content

        if trueFalse == "TRUE":
            print("EMAIL SENT")

            # get a suitable subject line for the email
            subject_prompt = [{"role": "system", "content": "Using a conversation between a client and service deks technician, respond with a subject for an email to IT support to all further messages that you get. The converation will be a list of dictionaries"}]

            subject_prompt.append({"role": "user", "content": str(messages)}) 

            get_subject = openai.ChatCompletion.create(
                model="gpt-4",
                messages=subject_prompt,    
                max_tokens=150
            )

            subject_t = get_subject.choices[0].message.content

            # get a suitable body for the email
            body_prompt = [{"role": "system", "content": "Using a conversation between a client and service deks technician, respond with a suitable email body. Try to include the impact, what service is affected, how it is impacting business operations, and when the problem started. The clients name is {name}. Sign off the email with the name 'WESley'. The converation will be a list of dictionaries".format(request.user.username)}]

            body_prompt.append({"role": "user", "content": str(messages)})

            get_body = openai.ChatCompletion.create(
                model="gpt-4",
                messages=body_prompt,
                max_tokens=150
            )

            body_t = get_body.choices[0].message.content

            # send the email

            # Email configuration
            sender_email = 'askwesley589@gmail.com'
            sender_password = GMAIL_PASSWORD
            recipient_email = '23072152@student.uwa.edu.au'
            subject = subject_t
            message = body_t

            # Create a MIMEText object for the email content
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # SMTP server configuration (for Gmail)
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587

            # Establish a connection to the SMTP server
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)

                # Send the email
                server.sendmail(sender_email, recipient_email, msg.as_string())
                print('Email sent successfully')

            except Exception as e:
                print(f'An error occurred: {str(e)}')

            finally:
                # Close the SMTP server connection
                server.quit()

        # Return the processed result as JSON
        return JsonResponse({'result': processed_output})

    return JsonResponse({'error': 'Invalid request method'})

    


