from django.db import models
from django.contrib.auth.models import User # Import the User model
from datetime import date

class Task(models.Model):
    # Foreign Key to link tasks to users
    # on_delete=models.CASCADE means if a User is deleted, all their tasks are also deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True) # THIS IS CRUCIAL: Must allow null/blank
    status = models.CharField(max_length=20, default='in-progress')
    complete_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Corrected syntax here

    def __str__(self):
        return f"{self.user.username}'s Task: {self.description[:50]}"