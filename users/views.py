from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_user(request):
    if request.method != "POST":
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('test_app:index')
    context = {'form':form}
    return render(request, "registration/login.html", context)

def logout_user(request):
    logout(request)
    context = {}
    return render(request, "registration/logout.html", context)

def register(request):
    if request.method != "POST":
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("test_app:index")

    context = {"form":form}
    return render(request, "registration/register.html", context)