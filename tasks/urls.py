from django.urls import path
from tasks.views import showTask,showSpecificTask
urlpatterns = [
    path('show-task/',showTask),
    path('show-task/<int:id>/',showSpecificTask),
]
