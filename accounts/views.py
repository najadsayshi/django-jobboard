
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.


from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/accounts/dashboard/')  # redirects to role-based dashboard
        else:
            error = "Invalid username or password"
            return render(request, 'accounts/login.html', {'error': error})
    return render(request, 'accounts/login.html')


@login_required
def dashboard(request):
    user = request.user
    if user.role == 'employer':
        return render(request, 'accounts/employer_dashboard.html')
    elif user.role == 'student':
        return render(request, 'accounts/student_dashboard.html')
from django.contrib.auth import logout

@login_required
def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')
