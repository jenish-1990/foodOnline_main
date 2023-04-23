from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages
# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            # Create the user using the form
            # password = form.cleaned_data['password'] # get the password from the form
            # user = form.save(commit=False) # form is now ready to be saved but not yet saved. whatever data we have in form will be assigned to user object
            # user.set_password(password) # hashing the password
            # user.role = User.CUSTOMER # now we assign the role of customer
            # user.save()

            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered successfully!")
            return redirect('registerUser')
    
    else:
        form = UserForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)