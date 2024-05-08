from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from authentication.forms import login_modal_form

# Create your views here.
def index_view (request): 
    return render(request, 'authentication/index.html')

def login_modal (request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            print("login invalid")
    return render(request, 'login_form.html')
