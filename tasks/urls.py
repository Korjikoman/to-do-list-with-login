from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.signup),
    path('index/', views.index, name="list"),
    path('loginn/', views.loginn, name="loginn"),
    path('update_task/<str:pk>/', views.updateTask, name="update_task"),
    path('delete/<str:pk>/', views.deleteTask, name="delete"),
    path('set_tas_to_done/<str:pk>/', views.set_task_to_done, name="set_task_to_done")
]
