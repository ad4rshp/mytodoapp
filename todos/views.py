from .models import Task
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import date
from django.contrib.auth.models import User # Ensure User model is imported for clarity
from django.contrib import messages

# Helper function to get the CSRF token for AJAX requests
def get_csrf_token(request):
    from django.middleware.csrf import get_token
    return JsonResponse({'csrftoken': get_token(request)})

@login_required
def index(request):
    """
    Renders the main To-Do application page.
    Requires user to be logged in.
    """
    return render(request, 'todoapp.html')

@csrf_exempt
@require_http_methods(["GET", "POST"])
def signup_view_func(request):
    """
    Handles user registration.
    GET: Displays the signup form.
    POST: Processes form submission, creates user, logs them in, and redirects.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! You are now logged in.')
            return redirect('/')
        else:
            print("Signup Form Errors:", form.errors)
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def login_view_func(request):
    """
    Handles user login.
    GET: Displays the login form.
    POST: Authenticates user and logs them in.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
                print("Login Form Errors (Authentication Failed): No user found with credentials matching provided input.")
                return render(request, 'login.html', {'form': form})
        else:
            print("Login Form Errors (Validation Failed):", form.errors)
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

@login_required
def custom_logout_view(request):
    """
    Logs out the current user and redirects to the login page.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def tasks_api_list_create(request):
    """
    API endpoint for listing and creating tasks.
    GET: Returns a list of tasks for the authenticated user.
    Uses select_related to optimize fetching of related User data.
    """
    if request.method == 'GET':
        # Optimizing query: select_related fetches related 'user' object in the same query.
        # This prevents N+1 query problem if we later access properties of 'task.user'
        # in the loop, although for current API response, it's more for good practice/scalability.
        tasks = Task.objects.filter(user=request.user).select_related('user').order_by('-created_at')
        task_list = [
            {
                'id': task.id,
                'description': task.description,
                'due_date': str(task.due_date) if isinstance(task.due_date, date) else None,
                'status': task.status,
                'complete_date': str(task.complete_date) if isinstance(task.complete_date, date) else None
            }
            for task in tasks
        ]
        return JsonResponse(task_list, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        description = data.get('description')
        due_date_str = data.get('due_date')
        status = data.get('status', 'in-progress')

        due_date = date.fromisoformat(due_date_str) if due_date_str else None

        if not description:
            return JsonResponse({'error': 'Description is required.'}, status=400)
        
        task = Task.objects.create(
            user=request.user,
            description=description,
            due_date=due_date,
            status=status,
            complete_date=date.today() if status == 'complete' else None
        )
        return JsonResponse({
            'id': task.id,
            'description': task.description,
            'due_date': str(task.due_date) if isinstance(task.due_date, date) else None,
            'status': task.status,
            'complete_date': str(task.complete_date) if isinstance(task.complete_date, date) else None
        }, status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
@login_required
def tasks_api_retrieve_update_delete(request, pk):
    """
    API endpoint for retrieving, updating, and deleting a single task.
    Ensures that only tasks owned by the authenticated user can be accessed.
    """
    task = Task.objects.filter(pk=pk, user=request.user).first()

    if not task:
        return JsonResponse({'error': 'Task not found or not authorized'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': task.id,
            'description': task.description,
            'due_date': str(task.due_date) if isinstance(task.due_date, date) else None,
            'status': task.status,
            'complete_date': str(task.complete_date) if isinstance(task.complete_date, date) else None
        })
    
    elif request.method in ['PUT', 'PATCH']:
        data = json.loads(request.body)
        
        new_description = data.get('description')
        if new_description is not None:
            task.description = new_description

        new_due_date_str = data.get('due_date')
        if new_due_date_str is not None:
            task.due_date = date.fromisoformat(new_due_date_str) if new_due_date_str else None

        new_status = data.get('status', task.status)
        if new_status != task.status:
            task.status = new_status
            if new_status == 'complete':
                task.complete_date = date.today()
            else:
                task.complete_date = None

        task.save()
        return JsonResponse({
            'id': task.id,
            'description': task.description,
            'due_date': str(task.due_date) if isinstance(task.due_date, date) else None,
            'status': task.status,
            'complete_date': str(task.complete_date) if isinstance(task.complete_date, date) else None
        })

    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Task deleted successfully'}, status=204)