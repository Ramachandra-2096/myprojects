from django.db import models
from django.contrib.auth.models import User

class Interest(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    company_name = models.CharField(max_length=225)
    gstin = models.CharField(max_length=225)
    created_date = models.DateField()
    company_code = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    interests = models.ManyToManyField(Interest, related_name='users', blank=True)
    profile_image = models.ImageField(upload_to='static/profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    projects = models.CharField(max_length=225)
    date = models.DateTimeField()

    def __str__(self):
        return self.projects

class ChatMessage_hack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

class Connection(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

from django.db import models

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    due_time = models.TimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return self.title

from django.db import models

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_file = models.FileField(upload_to='myprojects/Nitk_hack/uploads')
    project_name = models.CharField(max_length=252)
