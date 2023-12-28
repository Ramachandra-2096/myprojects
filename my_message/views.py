from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from my_message.models import ChatMessage
from django.contrib.auth.decorators import login_required
from my_message.forms import LoginForm, SignUpForm
from django.contrib.auth import login as auth_login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        redirect_url = '/custom_login'
        return redirect(redirect_url)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

def custom_login(request):
    login_form = LoginForm()
    signup_form = SignUpForm()
    if request.method == 'POST':
        if 'login-submit' in request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Login successful!')
                    return redirect('chat', permanent=True)  # 'permanent=True' will cause a 301 redirect  
                else:
                    messages.error(request, 'Invalid username or password')
            else:
                messages.error(request, 'Login form is not valid')
                print(form.errors)
        elif 'signup-submit' in request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                auth_login(request, user)
                messages.success(request, 'Signup successful!')
                return redirect('chat')
            else:
                messages.error(request, 'Signup form is not valid')
                print(form.errors)

    return render(request, 'my_message/index.html', {'login_form': login_form, 'signup_form': signup_form})

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage

@login_required
def chat_view(request):
    if request.method == 'POST':
        user = request.user
        message_content = request.POST.get('message_input')
        if message_content:
            ChatMessage.objects.create(user=request.user, content=message_content)
            return JsonResponse({'status': 'success'})
    messages = ChatMessage.objects.all()
    return render(request, 'my_message/home.html', {'messages': messages})

@login_required
def get_messages(request):
    user = request.user
    messages = ChatMessage.objects.all()
    messages_data = [{'user': message.user.first_name, 'content': message.content,'timestamp': message.timestamp, 'is_mine': message.user == request.user} for message in messages]
    return JsonResponse({'messages': messages_data})