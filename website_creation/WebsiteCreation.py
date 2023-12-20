from django.http import HttpResponse
import shutil
import os
import time
from .mod_create_website import website_creation as wc
from .mod_string_es import strings as es
from .mod_string_de import strings as de
from .mod_string_en import strings as en
from .mod_string_kn import strings as kn
from .mod_string_hi import strings as hi

def create_main(lang, name, uploaded_file, template):
    if lang == "Deutsch":
        s1, s2, s3, s4,s5,s6,s7 = de()
    elif lang == "Española":
        s1, s2, s3, s4,s5,s6,s7 = es()
    elif lang == 'Kannada':
        s1, s2, s3, s4,s5,s6,s7 = kn()
    elif lang == 'Hindi':
        s1, s2, s3, s4,s5,s6,s7 = hi()
    else:
        s1, s2, s3, s4 ,s5,s6,s7 = en()

    def time1():
        import datetime as dt
        today = dt.datetime.now()
        y1 = str(today.year)
        m1 = str(today.month).zfill(2)
        d1 = str(today.day).zfill(2)
        h1 = str(today.hour).zfill(2)
        m2 = str(today.minute).zfill(2)
        s2 = str(today.second).zfill(2)
        fname2 = '_' + y1 + m1 + d1 + '_' + h1 + m2 + s2
        return fname2

    college = name
    result = wc(college, uploaded_file, template)
    
    output_zip = 'WebsiteCreation_' + college + time1()
    output_zipfile = os.path.join('website_creation/static', output_zip)
    shutil.make_archive(output_zipfile, 'zip', os.path.join('website_creation/dirs', college))
    
    s5 =f"{output_zip}.zip {s4}"
    time.sleep(1)
    shutil.rmtree(os.path.join('website_creation/dirs', college))
    s1=f"{output_zip}.zip "+s1
    with open(output_zipfile + '.zip', 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_zipfile)}.zip"'
    os.remove(output_zipfile + '.zip')
    return (response,s5,s1)
