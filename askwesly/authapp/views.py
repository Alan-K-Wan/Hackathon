# authapp/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def secret_page(request):
    # Access the user's name
    user_name = request.user.username

    # Pass the user's name to the template
    context = {'user_name': user_name}
    return render(request, 'authapp/secret_page.html', context)

@login_required
def process_input(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')

        # Process the input (you can replace this with your actual processing logic)
        processed_output = "You entered: " + input_text  # Modify this line with your processing logic

        # Return the processed result as JSON
        return JsonResponse({'result': processed_output})

    return JsonResponse({'error': 'Invalid request method'})

    


