# mytodoapp/todos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Main To-Do application page (e.g., yourdomain.com/)
    # CHANGE THIS LINE: views.todo_app_homepage -> views.index
    path('', views.index, name='todo_list'), 

    # Authentication URLs
    path('signup/', views.signup_view_func, name='signup'),
    path('login/', views.login_view_func, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    
    # API endpoints for tasks
    path('api/tasks/', views.tasks_api_list_create, name='api_tasks_list_create'),
    path('api/tasks/<int:pk>/', views.tasks_api_retrieve_update_delete, name='api_tasks_retrieve_update_delete'),
    path('api/get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
]