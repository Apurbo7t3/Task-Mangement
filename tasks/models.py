from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        default=1,
        related_name='tasks'
    )
    assigned_to = models.ManyToManyField(
        Employee,
        related_name='tasks'
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_completed = models.BooleanField(default=False) 
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    TASK_PRIORITIES = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    )

    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name='details'
    )

    priority = models.CharField(max_length=1, choices=TASK_PRIORITIES)
    notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'Details for Task {self.task.title}'