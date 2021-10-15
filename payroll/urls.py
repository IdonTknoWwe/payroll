"""payroll URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apps.user.views import LoginRender, DashboardView
from django.conf.urls.static import static
from django.conf import settings

# from aplicaciones.enterprises import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^configuration/', include('apps.administracion.urls', namespace ='Administracion')),
    url(r'^employee/', include('apps.employee.urls', namespace ='Empleados')),
    url(r'^enterprise/', include('apps.enterprise.urls', namespace ='Empresas')),
    url(r'^client/', include('apps.cliente.urls', namespace ='Clientes')),
    url(r'user/', include('apps.user.urls', namespace ='Usuarios')),
    url(r'^dashboard/', DashboardView.as_view(), name="Dashboard"),
    url(r'^$', LoginRender, name='login'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
