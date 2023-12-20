import os
from django.shortcuts import render
from .forms import submit_form
from .WebsiteCreation import create_main
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .mod_string_es import strings as es
from .mod_string_de import strings as de
from .mod_string_en import strings as en 
from .mod_string_kn import strings as kn
from .mod_string_hi import strings as hi

def set_cookie(request):
    if request.method == 'POST':
        lang = request.POST.get('choice_field')
        response = HttpResponseRedirect('make_zip')  
        response.set_cookie('selected_value', lang)
        return response
    return render(request, 'index.html')

def shtml(request):
    file_path = 'template/template2.html'
    with open(file_path, 'rb') as f1:
        response = HttpResponse(f1.read(), content_type='text/html')  
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response 

def stxt(request):
    file_path = 'template/StudentWebsite.txt'
    with open(file_path, 'rb') as f1:
        response = HttpResponse(f1.read(), content_type='text/html')  
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response 

def make_zip(request):
    lang  = request.COOKIES.get('selected_value', 'English')
    if lang == 'Deutsch':
        cname = de()
    elif lang == 'Española':
        cname = es()
    elif lang == 'Kannada':
        cname = kn()
    elif lang == 'Hindi':
        cname = hi()
    else :
        cname = en()
    my_dict = {
        "name": cname[1],
        "template": cname[2],
        "sample":cname[4],
        "txt": cname[5],
        "gen": cname[6],
    }
    form = submit_form()
    if request.method == 'POST':
        form = submit_form(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            template = form.cleaned_data.get('template')
            uploaded_file = form.cleaned_data.get('file')
            
            destination = os.path.join('static',uploaded_file.name)
            destination1 =os.path.join('static',template.name)
            try:
                with open(destination, 'wb+') as destination_file:
                        destination_file.write(uploaded_file.read())
                        
                with open(destination1, 'wb+') as destination_file:
                        destination_file.write(template.read())  
                print("Language"+lang)    
                response,a,b = create_main(lang, name, destination, destination1)
                messages.success(request,a)
                messages.success(request,b)
                
                refresh_delay = 1000
                response.write(f'<script>setTimeout(function(){{window.location.reload(true);}}, {refresh_delay});</script>')
                return response
            except Exception as e:
                form =submit_form()
                response = HttpResponse(f"Error :{e}")
                return response
    else:
        form = submit_form()
        
    return render(request, 'template.html', {'form': form,'my_dict':my_dict})



