from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login as auth_login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm, SignUpForm
from django.contrib.auth.views import LoginView

def land(request):
    return render(request,"Nitk_hack/land.html")

from django.views import View
class DummyDataView(View):
    def get(self, request, *args, **kwargs):
        completed_projects_data = {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'company_projects': [10, 20, 15, 25, 30],
            'user_projects': [5, 15, 10, 20, 25],
        }

        return JsonResponse(completed_projects_data)
@csrf_exempt    
def custom_login(request):  ##RUNNING
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
                    return redirect('home', permanent=True) 
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
                return redirect('user_profile')
            else:
                messages.error(request, 'Signup form is not valid')
                print(form.errors)

    return render(request, 'Nitk_hack/login.html', {'login_form': login_form, 'signup_form': signup_form})

from django.shortcuts import render, redirect
from django.views import View
from .models import ChatMessage_hack, Company, Project
import uuid

def generate_unique_code():  ##RUNNING
    unique_code = str(uuid.uuid4())
    return unique_code
@csrf_exempt
class CompanySignupView(View):  ##RUNNING
    template_name = 'Nitk_hack/company_Register.html'
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        company_name = request.POST.get('companyName')
        gst_code = request.POST.get('code')
        date_of_creation = request.POST.get('dateOfCreation')
        if Company.objects.filter(company_name=company_name, gstin=gst_code).exists():
            return render(request, self.template_name, {'error_message': 'Duplicate combination of company name and GST code'})
        code =generate_unique_code()
        company = Company.objects.create(
            company_name=company_name,
            gstin=gst_code,
            created_date=date_of_creation,
            company_code=code
        )
        return render(request,'Nitk_hack/company_Register.html',{'code':code}) 
    
@login_required
def home(request):   ##RUNNING
    user=request.user
    user_profile = UserProfile.objects.get(user=user)
    profile_image_url = user_profile.profile_image.url
    return render(request,'Nitk_hack/home.html',{'user':user,'profile':profile_image_url})

@login_required
def meet(request):   ##RUNNING
    user =request.user
    return render(request,'Nitk_hack/WEB_UIKITS.html',{'username':user.first_name})

@login_required
def Custom_logout(request): ##RUNNING
    logout(request)
    return redirect('custom_login')


from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage_hack
@csrf_exempt
@login_required
def chat_view(request):
    if request.method == 'POST':
        user = request.user
        profile = UserProfile.objects.get(user=user)
        message_content = request.POST.get('message_input')
        if message_content:
            ChatMessage_hack.objects.create(user=request.user,company=profile.company, content=message_content)
            return JsonResponse({'status': 'success'})
    profile = UserProfile.objects.get(user=request.user)
    messages = ChatMessage_hack.objects.filter(company=profile.company)
    return render(request, 'Nitk_hack/chat.html', {'messages': messages,'c':profile.company})

@login_required
def get_messages(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    messages = ChatMessage_hack.objects.filter(company=profile.company)
    messages_data = [{'user': message.user.first_name, 'content': message.content,'timestamp': message.timestamp, 'is_mine': message.user == request.user} for message in messages]
    return JsonResponse({'messages': messages_data})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile, Company
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
@csrf_exempt
@login_required
def user_profile(request):  ##RUNNING
    user = request.user
    if UserProfile.objects.filter(user=user).exists():
        return redirect('home')
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile_data = form.cleaned_data
            company = get_object_or_404(Company, company_code=user_profile_data['company_code'])
            profile, created = UserProfile.objects.get_or_create(user=user, defaults={'company': company})
            profile.birth_date = user_profile_data['birth_date']
            profile.profile_image = user_profile_data['profile_image']
            profile.interests.set(user_profile_data['interests'])
            profile.save()

            return redirect('home')
    else:
        form = UserProfileForm()
    return render(request, 'Nitk_hack/servay.html', {'form': form})

from django.http import JsonResponse
from django.shortcuts import render
from .models import Task

def index(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'Nitk_hack/index.html', {'tasks': tasks})
@csrf_exempt
def create(request):
    user=request.user
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        description = request.POST.get('description')
        due_time = request.POST.get('due_time')
        task = Task.objects.create(user=user,title=title, due_date=due_date, due_time=due_time, description=description)
        return JsonResponse({'status': 'ok'})
@csrf_exempt
def update(request, pk):
    if request.method == 'POST':
        task = Task.objects.get(user=request.user,pk=pk)
        task.completed = not task.completed
        task.save()
        return JsonResponse({'status': 'ok'})
@csrf_exempt
def delete(request, pk):
    if request.method == 'POST':
        task = Task.objects.get(user=request.user,pk=pk)
        task.delete()
        return JsonResponse({'status': 'ok'})


from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Connection
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class UserListView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.exclude(id=request.user.id)
        connections = Connection.objects.filter(from_user=request.user)
        profile_image_urls = []

        for user in users:
            try:
                user_profile = UserProfile.objects.get(user=user)
                profile_image_urls.append({'user': user, 'image_url': user_profile.profile_image.url})
            except UserProfile.DoesNotExist:
                profile_image_urls.append({'user': user, 'image_url': ''})

        context = {
            'users': users,
            'connections': connections,
            'profile_image_urls': profile_image_urls,
        }

        return render(request, 'Nitk_hack/user_list.html', context)
    
@csrf_exempt  
class FollowToggleView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        user_to_follow = User.objects.get(id=user_id)
        connection_exists = Connection.objects.filter(from_user=request.user, to_user=user_to_follow).exists()
        if connection_exists:
            Connection.objects.filter(from_user=request.user, to_user=user_to_follow).delete()
            status = 'unfollowed'
        else:
            Connection.objects.create(from_user=request.user, to_user=user_to_follow)
            status = 'followed'
        return JsonResponse({'status': status})

from django.shortcuts import render, redirect
from .forms import ProjectUploadForm
@login_required
def upload_project(request):
    if request.method == 'POST':
        form = ProjectUploadForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user=request.user
            project.save()
            return redirect('home')
    else:
        form = ProjectUploadForm()

    return render(request, 'Nitk_hack/upload.html', {'form': form})

# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse

def file_list(request):
    files = Project.objects.all()
    return render(request, 'Nitk_hack/file_list.html', {'files': files})
@csrf_exempt
def download_file(request, file_id):
    file = Project.objects.get(id=file_id)
    response = HttpResponse(file.project_file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename={file.project_file}'
    return response
