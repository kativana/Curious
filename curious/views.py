from django.shortcuts import render, redirect
from .models import Profile, Cueet
from .forms import CueetForm, LoginForm, RegistrationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse 
from django.contrib import messages


# Create your views here.

def dashboard(request):
    form = CueetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            cueet = form.save(commit=False)
            cueet.user = request.user
            cueet.save()
            return redirect("curious:dashboard")

    followed_cueets = Cueet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")

    return render(request, "curious/dashboard.html", 
    {"form": form, "cueets":followed_cueets},
    )

def profile_list(request):
    profiles = Profile.objects.exclude(user = request.user)
    return render(request, "curious/profile_list.html", {"profiles": profiles})

def profile(request, pk):
    if not hasattr(request.user, "profile"):
        missing_profile = Profile(user=request.user)
        missing_profile.save()


    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "curious/profile.html", {"profile": profile})


def register(request):

    if request.method == "GET":
        return render(
            request, "registration/register.html",
            {"form": RegistrationForm}
        )

    elif request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            #messages.success(request, 'Congrats, you have successfully registered!')
            return redirect(reverse("login"))
        else:
            messages.error(request, 'Sorry, the registration was unsuccessful. Please check the requirements and try again!')
            messages.error(request, form.errors)
            return render(
            request, "registration/register.html",
            {"form": RegistrationForm}
        )
    
    form = RegistrationForm()
    return render (request, "registration/login.html", 
    {"form":LoginForm})


def login_fun(request):
    return render(request, "curious/login.html", {"LoginForm": LoginForm})