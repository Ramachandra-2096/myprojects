from django.urls import path
from todolist.views import index,create,update,delete
urlpatterns = [
    path('', index, name='index'),
    path('create/', create, name='create'),
    path('update/<int:pk>/', update, name='update'),
    path('delete/<int:pk>/', delete, name='delete'),
]