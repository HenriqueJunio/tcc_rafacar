from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from rafacar.views import home

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # tela inicio
    path('home', home, name='home'),
    path('contato/', views.contato, name='contato'),
    path('sobre/', views.sobre, name='sobre'),
    path('servicos/', views.servicos, name='servicos'),
    path('login/', views.login_user, name='login'),
    path('cadastro/', views.cadastrar_usuario, name='cadastro'),
    path('agendar/', views.agendar, name='agendar'),
    path('agendamentos/', views.agendamentos, name='agendamentos'),
    path('area_membros/', views.area_membros, name='area_membros'),
    path('agendamentos/excluir/<int:agendamento_id>/', views.excluir_agendamento, name='excluir_agendamento'),
    path('agendamentos/editar/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'),
    path('edita_user/', views.edita_user, name='edita_user'),
    path('agendamentos_gestor/', views.agendamentos_gestor, name='agendamentos_gestor'),
    path('logout/', views.logout_view, name='logout'),
]   

