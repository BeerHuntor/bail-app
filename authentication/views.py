from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from authentication.forms import LoginModalForm, UserForm, UserProfileInformation
from django.views.generic.edit import FormView

auth_redirect_url = 'https://discord.com/oauth2/authorize?client_id=1228365653254209606&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2F&scope=identify+guilds+connections'

# Create your views here.
def index_view (request): 
    form = LoginModalForm()
    return render(request, 'authentication/index.html', {'form' : form})

def login_modal (request):
    if request.method == 'POST':
        form = LoginModalForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect(reverse_lazy('authentication:index'))
            else:
                print("not a registered user")
        else:
            print("login invalid")


    else: 
        form = LoginModalForm()
    return render(request, 'authentication/login_form.html', {'form': form })

class RegisterModalView (FormView):
    user_form_class = UserForm
    profile_info_form_class = UserProfileInformation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = self.user_form_class
        context['profile_form'] = self.profile_info_form_class
        return context
    
    def form_valid(self, form):
        user = form.save

    def get_template_names(self):
        return ['authentication:register']
    

    