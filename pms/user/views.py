from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from .models import User
from .forms import ManagerRegisterForm,DeveloperRegistrationForm,AdminRegisterForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView,ListView,DetailView
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from project.views import *
from user.decorators import *
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



class AdminRegisterView(CreateView):
    model = User
    form_class = AdminRegisterForm
    template_name = 'user/admin_register.html'
    #success_url = "/product/adminpage/"
    
    def form_valid(self,form):
        email = form.cleaned_data.get('email')
        user=form.save()
        recipient_list = [email]
        subject = "welcome to django"
        message = "Say hello to Django!! You are Admin now"
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
        #print(email)
        login(self.request,user)
        return redirect('/user/adminpage/')


class ManagerRegisterView(CreateView):
    model = User
    form_class = ManagerRegisterForm
    template_name = 'user/manager_register.html'
    #success_url = "/product/managerpage/"
    
    def form_valid(self,form):
        email = form.cleaned_data.get('email')
        user=form.save()
        recipient_list = [email]
        subject = "welcome to django"
        message = "Say hello to Django!! You are Manager now"
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
        #print(email)
        login(self.request,user)
        return redirect('/user/managerpage/')

        

class DeveloperRegisterView(CreateView):
    model = User
    form_class = DeveloperRegistrationForm
    template_name = 'user/developer_register.html'
    #success_url = "/product/developerpage/"    

        
    def form_valid(self,form):
        email = form.cleaned_data.get('email')
        user=form.save()
        recipient_list = [email]
        subject = "welcome to django"
        message = "Say hello to Django!! You are Developer now"
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
        #print(email)
        login(self.request,user)
        return redirect('/user/developerpage') 

    

class UserLoginView(LoginView):
     template_name = 'user/login.html'
     #success_url = "/"
    
     def get_redirect_url(self):
         if self.request.user.is_authenticated:
             if self.request.user.is_manager:
                 return '/user/managerpage/'
             else:
                 return '/user/developerpage/'
            
def sendMail(request):
    subject = "welcome to django"
    message = "hello django"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [User.objects.values_list('email', flat=True)]
    send_mail = (subject,message,email_from,recipient_list)

    return HttpResponse("mail sent")



def logoutUser(request):
    logout(request)
    return redirect('index')


class UserProfileView(TemplateView):
    template_name = "user/user_profile.html"


@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class AdminPage(TemplateView):
    template_name="user/admin_page.html"

# @method_decorator(login_required(login_url='/user/login'), name='dispatch')
@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ManagerPage(ListView):

    def get(self,request,*args,**kwargs):
        project = Project.objects.all().values()
        team = Project_Team.objects.all().values()
        completedproject = Project.objects.filter(status="Completed")
        pendingproject = Project.objects.filter(status="Pending")
        return render(request, 'user/manager_page.html',{'projects':project,'teams':team,'completedprojects':completedproject,'pendingprojects':pendingproject})

    template_name="user/manager_page.html"

@method_decorator([login_required(login_url="/user/login"),developer_required],name='dispatch')
class DeveloperPage(TemplateView):
    template_name="user/developer_page.html"


# @method_decorator(csrf_exempt, name='dispatch')
# class ProjectChartView(TemplateView):
#     template_name = 'user/manager_page.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         completed_projects = Project.objects.filter(status='Completed').count()
#         pending_projects = Project.objects.filter(status='Pending').count()
#         context['completed_projects'] = completed_projects
#         context['pending_projects'] = pending_projects
#         return context

def project_chart(request):
    completed_projects = Project.objects.filter(status='Completed').count()
    pending_projects = Project.objects.filter(status='Pending').count()

    context = {
        'completed_projects': completed_projects,
        'pending_projects': pending_projects,
    }
    return render(request, 'user/manager_page.html', context)