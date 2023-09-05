# authapp/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def secret_page(request):
    # Access the user's name
    user_name = request.user.username

    # Pass the user's name to the template
    context = {'user_name': user_name}
    return render(request, 'authapp/secret_page.html', context)

    


