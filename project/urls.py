from django.urls import path
from . import views

urlpatterns = [
    path('project/', views.index, name='index'),
    path('', views.project_list, name='project_list'),  
    path('create/', views.project_create, name='project_create'),
    path('<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('register/', views.register, name='register'),
]
