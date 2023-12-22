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
                    return redirect('home', permanent=True)  # 'permanent=True' will cause a 301 redirect  
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
                return redirect('home')
            else:
                messages.error(request, 'Signup form is not valid')
                print(form.errors)

    return render(request, 'my_message/index.html', {'login_form': login_form, 'signup_form': signup_form})

@login_required
def chat_view(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:
            ChatMessage.objects.create(user=request.user, content=message_content)
            return JsonResponse({'status': 'success'})
    user =request.user
    company = user.company
    messages = ChatMessage.objects.filter(company=company)
    return render(request, 'my_message/home.html', {'messages': messages})

# views.py
from django.http import JsonResponse

@login_required
def get_messages(request):
    messages = ChatMessage.objects.all()
    messages_data = [{'user': message.user.username, 'content': message.content} for message in messages]
    return JsonResponse({'messages': messages_data})
