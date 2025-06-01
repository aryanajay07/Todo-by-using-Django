from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('todo/', views.todo, name='todo'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('edit-todo/<int:todo_id>/', views.edit_todo, name='edit_todo'),
]
