from django.shortcuts import render
from .models import UserProfileInfo
from django.contrib.auth.models import User
from .forms import UserProfileInfoForm, UserForm

# For the login page
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html', context={'on_index':True})

def cats(request):
    return render(request, 'basic_app/cats.html', context={'on_cats':True})

# The user must be logged in to be able to use this function
@login_required 
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password) # HASH the password with set_password()
            user.save()

            profile = profile_form.save(commit=False) # Don't commit yet because there may be some conflicts
            profile.user = user

            # Check if there is a picture in the registration
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            # Errors if something was not valid
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', 
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered,
                   'on_register':True})

# Make sure we don't call it login because that is an imported function
def user_login(request):
    if request.method == "POST":
        # username and password was the name of the inputs that we defined in the html template
        username = request.POST.get('username')
        password = request.POST.get('password') 

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                # return HttpResponseRedirect(reverse('index'))
                return index(request)

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid login details supplied!<p></p>"
                                 "<a href=''>Try again</a>")

    else:
        return render(request, 'basic_app/login.html', context={'on_login':True})
