from django.urls import path,include
from .views import *
from . import views

urlpatterns = [
 path('addprojects/',AddProjectsView.as_view(),name="addprojects"),
 path('addprojectsmodules/',AddProjectModulesView.as_view(),name="addprojectsmodules"),
 path('addprojectstask/',AddProjectTaskView.as_view(),name="addprojectstask"),
 path('addprojectsteam/',AddProjectTeamView.as_view(),name="addprojectsteam"),
 path('addusertask/',UserTaskView.as_view(),name="addusertask"),
 path('yourtask/',YourTask.as_view(),name="yourtask"),
 path('projectlist/',ProjectListView.as_view(),name="projectlist"),
 path('projectdelete/<int:pk>',ProjectDeleteView.as_view(),name='projectdelete'),
 path('projectupdate/<int:pk>',ProjectUpdateView.as_view(),name='projectupdate'),
 path('projectdetail/<int:pk>',ProjectDetailView.as_view(),name='projectdetail'),
]