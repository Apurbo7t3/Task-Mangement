from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.models import Employee,Task,Project
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from django.db.models import Q, Count,Sum,Avg
from django.contrib import messages
# Create your views here.
def manager_dashboard(request):
    request_type=request.GET.get('type','all')
    tasks=Task.objects.select_related('details').prefetch_related('assigned_to').all()
    counts=Task.objects.aggregate(
        total_task=Count('id'),
        completed_task=Count('id',filter=Q(status='COMPLETED')),
        in_progress_task=Count('id',filter=Q( status='IN_PROGRESS')),
        todo_task=Count('id',filter=Q(status='PENDING'))
    )
    if(request_type=='completed'):
        tasks=tasks.filter(status='COMPLETED')
    elif request_type=='in_progress':
        tasks=tasks.filter(status='IN_PROGRESS')
    elif request_type=='todo':
        tasks=tasks.filter(status='PENDING')
    
    context={
        'tasks':tasks,
        'counts':counts
    }
    return render(request,'dashboards/manager_dashboard.html',context)

def user_dashboard(request):
    return render(request,'dashboards/user_dashboard.html')

def test(request):
    context={
        'age':'Hello Apurbo'
    }
    return render(request,'test.html',context)

def create_task(request):
    if request.method=='POST':
        task_form=TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST)

        if task_form.is_valid() and task_detail_form.is_valid():
            """Django model form"""
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
            task_detail_form.save()
            messages.success(request, 'Task Added Successfully!')
            return redirect('task-form')
            """General method of form"""
            # data=form.cleaned_data
            # title=data.get('title')
            # description=data.get('description')
            # due_date=data.get('due_date')
            # assigned=data.get('assigned_to')
            # task=table1.objects.create(title=title,description=description,dueDate=due_date)
            # for emp_id in assigned:
            #     emp=Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(emp)
            # return HttpResponse("Form submitted successfully")

    task_form=TaskModelForm()
    task_detail_form=TaskDetailModelForm()
    context={
        'task_form':task_form,
        'task_detail_form': task_detail_form
    }
    return render(request,'task_form.html',context)

def update_task(request,id):
    task=Task.objects.get(id=id)
    if request.method=='POST':
        task_form=TaskModelForm(request.POST,instance=task)
        task_detail_form=TaskDetailModelForm(request.POST,instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():
            """Django model form"""
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
            task_detail_form.save()
            messages.success(request, 'Task Updated Successfully!')
            return redirect('update-form',id)
    if id :
        task_form=TaskModelForm(instance=task)
        task_detail_form=TaskDetailModelForm(instance=task.details)
        context={
            'task_form':task_form,
            'task_detail_form': task_detail_form
        }
        return render(request,'task_form.html',context)



def delete_task(request,id):
    if request.method=='POST':
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request,'Task Deleted SucessFully')
        return redirect('manager-dashboard')
    else:
        messages.error(request,'Something Went Wrong')
        return redirect('manager-dashboard')

def show_task(request):
    tasks=Project.objects.annotate(task_count=Count('tasks')).order_by('-task_count')
    return render(request,'show_task.html',{'tasks':tasks})