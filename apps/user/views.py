from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.core.urlresolvers import reverse_lazy
from apps.cliente.models import PermitsModel, ClienteModel
from braces.views import LoginRequiredMixin
from .models import UserModel, PermissionUser
from .forms import UserModelForm
from django.http import Http404
from django.core.exceptions import PermissionDenied
# Create your views here.

def LoginRender(request):
	if request.user.is_authenticated():
		return redirect('Dashboard')
	return render(request, 'templates/login/index.html')

def LoginView(request):
	user = authenticate(username=request.POST['username'], password=request.POST['password'])

	if user is not None:
		login(request, user)
		return redirect('Dashboard')
	else:
		return redirect('login')

def LogoutView(request):
	logout(request)
	return redirect('login')


class PermissionDashboard(object):
	def get_context_data(self, **kwargs):
		context = super(PermissionDashboard, self).get_context_data(**kwargs)
		if not self.request.user:
			raise Http404
		try:		
			usuario = PermitsModel.objects.filter(User=self.request.user)[0]
			permiso = usuario.permiso
			clientes = usuario.cliente.all()
			context['clientes'] = clientes
			context['permisos'] = False
			if permiso == 0 or permiso < 3:
				context['permisos'] = True

		except :
			pass
		return context

class PermissionMixin(object):
	def get_context_data(self, **kwargs):
		context = super(PermissionMixin, self).get_context_data(**kwargs)
		if not self.request.user:
			raise Http404
		try:		
			usuario = PermitsModel.objects.filter(user=self.request.user)[0]
			permiso = usuario.permiso
			context['permisos'] = False
			if permiso >= 3:
				raise PermissionDenied
			context['permisos'] = True
				
		except :
			raise PermissionDenied
		return context


class DashboardView(LoginRequiredMixin, PermissionDashboard,  TemplateView):
	template_name = 'templates/componentes/dashboard.html'

	login_url ='/'
	redirect_field_name = 'login'

class CreateUser(CreateView):
	model = UserModel
	form_class = UserModelForm
	template_name = 'templates/login/register.html'
	success_url = reverse_lazy('login')
