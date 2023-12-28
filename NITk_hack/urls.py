from django.urls import path
from .views import custom_login
from django.contrib import admin
from .views import custom_login,home,Custom_logout,meet,chat_view,get_messages,user_profile,CompanySignupView,land,index,create,update,delete,DummyDataView,UserListView, FollowToggleView,file_list, download_file,upload_project
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', land),
    path('custom_login/', custom_login, name='custom_login'),
    path('home/', home, name='home'),
    path('chat/', chat_view, name='chat'),
    path('meet/', meet, name='meet'),
    path('chat/', chat_view, name='chat_view'),
    path('user_profile', user_profile, name='user_profile'),
    path('signup/', CompanySignupView.as_view(), name='company_signup'),
    path('logout/', Custom_logout, name='logout'),
    path('get_messages/', get_messages, name='get_messages'),
    path('todo', index, name='index'),
    path('dummy-data/', DummyDataView.as_view(), name='dummy_data'),
    path('create/', create, name='create'),
    path('update/<int:pk>/',update, name='update'),
    path('delete/<int:pk>/',delete, name='delete'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('follow_toggle/', FollowToggleView.as_view(), name='follow_toggle'),
    path('upload/', upload_project, name='upload_project'),
    path('files/', file_list, name='file_list'),
    path('files/<int:file_id>/download/', download_file, name='download_file'),
]
