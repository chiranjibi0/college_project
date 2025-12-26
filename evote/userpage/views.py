from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from .models import Profile
from .forms import SignupForm
from candidates .models import Voter

# Create your views here

def index(request):
    return render(request,'index.html')



def index_view(request):
    return render(request, 'index.html')



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            age = form.cleaned_data['age']
            user_type = form.cleaned_data['user_type']

            user = User.objects.create_user(
                username=phone,
                email=email,
                password=password
            )

            Profile.objects.create(
                user=user,
                age=age,
                user_type=user_type
            )

            if user_type == 'voter':  # assuming 'voter' is one choice
                Voter.objects.create(
                    voter_name=phone,
                    voter_age=age,
                    voter_id_number=int(phone) if phone.isdigit() else 0
                )

            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = authenticate(request, username=phone, password=password)

        if user is None:
            messages.error(request, "Invalid phone or password")
            return render(request, 'login.html')

        if user.profile.user_type != user_type:
            messages.error(request, f"You must login as {user.profile.get_user_type_display()}")
            return render(request, 'login.html')

        login(request, user)
        messages.success(request, "Login successful")
        return redirect('/candidate_name/show_candidate')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')
