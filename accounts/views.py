from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def signup(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('products:home')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    """User profile page"""
    return render(request, 'accounts/profile.html')