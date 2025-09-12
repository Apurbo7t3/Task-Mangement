from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,test,create_task,show_task,update_task,delete_task
urlpatterns = [
    path('manager-dashboard/',manager_dashboard,name='manager-dashboard'),
    path('user-dashboard/',user_dashboard),
    path('test/',test),
    path('task-form/',create_task,name='task-form'),
    path('update-form/<int:id>/',update_task,name='update-form'),
    path('delete-task/<int:id>/',delete_task,name='delete-task'),
    path('show-task/',show_task),
]
