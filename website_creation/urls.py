from django.urls import path
from website_creation.views import set_cookie, make_zip,shtml,stxt

urlpatterns = [
    path('', set_cookie, name='set_cookie'),
    path('make_zip/', make_zip, name='make_zip'),
    path('sample/', shtml, name='sample'),
    path('sampletext/', stxt, name='sampletext'),
]