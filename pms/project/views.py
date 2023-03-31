from django.shortcuts import render
from django.views.generic import TemplateView,ListView,DetailView,UpdateView,DeleteView,View
from django.views.generic.edit import FormView,CreateView
from pms.project.forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.decorators import *
from plotly.offline import plot
import plotly.graph_objs as go
from django.shortcuts import render, get_object_or_404
import plotly.express as px

class IndexView(TemplateView):
    template_name = "project/index.html"


@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class AddProjectsView(CreateView):
    form_class = AddProjectsForm
    model = Project
    template_name = 'project/add_projects.html'
    success_url = '/project/projectlist/'

    def form_valid(self, form):
        return super().form_valid(form)

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class AddProjectModulesView(CreateView):
    form_class = ProjectModulesForm
    model = Project_Module
    template_name = 'project/add_projects_modules.html'
    success_url = '/project/projectlist/'

    def form_valid(self, form):
        return super().form_valid(form)
    
@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class AddProjectTaskView(CreateView):
    form_class = ProjectTaskForm
    model = Project_Task
    template_name = 'project/add_projects_task.html'
    success_url = '/project/projectlist/'

    def form_valid(self, form):
        return super().form_valid(form) 

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class AddProjectTeamView(CreateView):
    form_class = ProjectTeamForm
    model = Project_Team
    template_name = 'project/add_projects_team.html'
    success_url = '/project/projectlist/'

    def form_valid(self, form):
        return super().form_valid(form)

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class UserTaskView(CreateView):
    form_class = UserTaskForm
    model = User_Task
    template_name = 'project/add_user_task.html'
    success_url = '/project/projectlist/'

    def form_valid(self, form):
        return super().form_valid(form) 


@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'project_list'
    
    def get_queryset(self):
        return super().get_queryset() 

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = AddProjectsForm
    template_name = 'project/add_projects.html'
    success_url = '/project/projectlist/'

@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'
    context_object_name = 'projectdetail'
    
    def get(self, request, *args, **kwargs):
        team = Project_Team.objects.filter(project_id=self.kwargs['pk'])
        return render(request, self.template_name, {'projectdetail': self.get_object(),'team':team})
    
      
@method_decorator([login_required(login_url="/user/login"),manager_required],name='dispatch')
class ProjectDeleteView(DeleteView):
    model = Project
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    success_url = '/project/projectlist/'    


@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class TaskListView(ListView):
    # model = User_Task
    # template_name = 'project/task_list.html'
    # context_object_name = 'task_list'
    
    # def get_queryset(self):
    #     return super().get_queryset()


    model = Project_Team
    template_name = 'project/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        return super().get_queryset().filter(user__username=self.request.user.username)
    

# class ProjectListView(LoginRequiredMixin, ListView):
#     model = Project_Team
#     template_name = 'project/task_list.html'
#     context_object_name = 'tasks'

#     def get_queryset(self):
#         return super().get_queryset().filter(user=self.request.user.username)


class ProjectModuleGanttView(DetailView):
    model = Project
    template_name = 'project/modules_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        modules = project.project_module_set.all()
        df = []
        for module in modules:
            df.append({
                'Task': module.module_name,
                'Start': module.module_start_date,
                'Finish': module.module_completion_date,
                'Developer': module.user.username if module.user else '',
            })
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Developer")
        chart_div = fig.to_html(full_html=False)
        context['chart_div'] = chart_div
        context['modules'] = modules
        return context