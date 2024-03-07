from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import own_authenticate
from django.db import IntegrityError



# Kokeilu
def first_view(request):
    return render(request=request, template_name='index.html')


#Authenticate metodi ei toimi koska salasana ei ole hashattu.
#kirjoita oma authenticate metodi mikä hakee käyttäjän ja vertaa salasanoja palauttaen user objektin.
def logged_user(request):
    if (request.method == 'POST' and request.POST.get('username')):
        username = request.POST['username']
        password = request.POST['pwd']
        us = own_authenticate(username=username, password=password)
        # use this with fixed password hashing.
        # us = authenticate(username=username, password=password)
        if us is not None:
            login(request, us)
            return render(request, 'index.html', {'username' : us.username})
        else:
            messages.error(request, "Incorrect account information!")

    return render(request=request, template_name='login.html')


def signup(request):
    if (request.method == 'POST' and request.POST.get('username') and request.POST.get('pwd')):
        # This does not hash password and allows it to be retreived in clear text.
        # This possibly allows injection of sql queries as username. Needs to be sanitised.
        user = User(username=request.POST['username'], password=request.POST['pwd']) # Create user object.
        # Under is properly hashed password.
        #user = User.objects.create_user(request.POST['username'], request.POST['pwd'])
        
        try: # If username is taken exception is raised.
            user.save() # Create new row for user object into database
        except IntegrityError:
            messages.error(request, "Username already taken!")
            return render(request, 'register.html')
        
        #return render(request, 'regcomp.html')
        return redirect('registered') #Loads confirmation page
    else:
        messages.error(request, "Invalid inputs!")
    return render(request, 'register.html')


def show_registered(request):
    if request.method == 'POST':
        if request.POST['form1_id'] == 'log':
            return redirect('login')
        if request.POST['form2_id'] == 'front':
            return redirect('')
    return render(request, "regcomp.html")


# Performs logging out.
def sign_out(request):
    logout(request)
    request.user = AnonymousUser()
    return redirect('home') # Use name parameter for redirect!

