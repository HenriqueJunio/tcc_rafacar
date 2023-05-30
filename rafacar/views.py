from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from .models import Agendamento, DadosPessoais


# Create your views here.
def home(request):
    return render(request, 'index.html')


def contato(request):
    return render(request, 'contato.html')


def sobre(request):
    return render(request, 'sobre.html')


def servicos(request):
    return render(request, 'servicos.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            if request.user.is_staff:
                return redirect('agendamentos')
            else:
               return redirect('home')

        else:
            # Autenticação falhou
            error_message = "Nome de usuário ou senha inválidos."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        # Exibição do formulário de login
        return render(request, 'login.html')


def cadastrar_usuario(request):
    mensagem_email_cadastrado = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        cep = request.POST.get('cep')
        endereco = request.POST.get('endereco')
        numero_casa = request.POST.get('numero_casa')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')

        if password1 != password2:
            # Senhas não coincidem.
            return redirect('senhas diferentes')

        if User.objects.filter(email=email).exists():
            # E-mail já está cadastrado.
            mensagem_email_cadastrado = 'E-mail já está cadastrado'
            return render(request, 'cadastro.html',
                            {'mensagem_email_cadastrado': mensagem_email_cadastrado})

        # Criação do usuário
        user = User.objects.create_user(
            username=username, password=password1, email=email)

        # Criação dos dados pessoais
        dados_pessoais = DadosPessoais(user=user, nome=nome, telefone=telefone,
                                       cep=cep, endereco=endereco,
                                       numero_casa=numero_casa, bairro=bairro,
                                       cidade=cidade)
        dados_pessoais.save()

        # Efetuar o login após o cadastro
        login(request, user)

        # redirecionar para a página inicial após o cadastro
        return redirect('home')

    return render(request, 'cadastro.html')


def agendar(request):
    mensagem_sucesso = None
    cadastro_existente = None

    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Faça login primeiro.')
        return redirect('login')

    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']
        endereco = request.POST['w3review']
        nivel = request.POST['nivel']
        preco = request.POST.get('preco')
        user = request.user  # Obtém o usuário logado

        if Agendamento.objects.filter(date=date, time=time).exists():
            cadastro_existente = 'Já existe um agendamento para esse dia e horário.'
            return render(request, 'index.html', {'cadastro_existente': cadastro_existente})

        dados_pessoais, _ = DadosPessoais.objects.get_or_create(user=user)

        try:
            agendamento = Agendamento.objects.get(
                user=user, dados_pessoais=dados_pessoais, date=date, time=time)
            agendamento.endereco = endereco
            agendamento.preco = preco
            agendamento.nivel = nivel
            agendamento.save()
        except Agendamento.DoesNotExist:
            agendamento = Agendamento.objects.create(
                user=user, dados_pessoais=dados_pessoais, date=date, time=time,
                endereco=endereco, preco=preco, nivel=nivel)

        mensagem_sucesso = "Agendamento concluido com sucesso!"

        return render(request, 'index.html', {'mensagem_sucesso': mensagem_sucesso})

    return render(request, 'agendar.html')


def agendamentos(request):
    """Agendamentos do usuário"""
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Faça login primeiro.')
        return redirect('login')

    if request.user.is_staff:
        agendamentos = Agendamento.objects.all().select_related('user', 'dados_pessoais')
        return render(request, 'agendamentos_gestor.html', {'agendamentos': agendamentos})

    # Filtra os agendamentos do usuário logado
    agendamentos = Agendamento.objects.filter(user=request.user)
    return render(request, 'agendamentos.html', {'agendamentos': agendamentos})


def excluir_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    agendamento.delete()
    return redirect('agendamentos')


def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, pk=agendamento_id)

    if request.method == 'POST':
        # Atualizar os campos do agendamento com base nos dados enviados no formulário
        agendamento.date = request.POST['date']
        agendamento.time = request.POST['time']
        agendamento.nivel = request.POST['nivel']

        # Salvar as alterações no banco de dados
        agendamento.save()

        # Redirecionar para uma página de confirmação ou detalhes do agendamento
        return redirect('agendamentos')

    # Caso contrário, exibir o modal com o formulário de edição
    return render(request, 'agendamentos.html', {'agendamento': agendamento})


def area_membros(request):
    """Area membros"""
    return render(request, 'area_membros.html')

def edita_user(request):
    """view para usuários editar seus dados pessoais"""
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Faça login primeiro.')
        return redirect('login')

    dados_pessoais = DadosPessoais.objects.filter(user=request.user).first()
    mensagem_sucesso = None

    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        cep = request.POST.get('cep')
        endereco = request.POST.get('endereco')
        numero_casa = request.POST.get('numero_casa')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')

        # Atualizar os campos relevantes
        dados_pessoais.nome = nome
        dados_pessoais.telefone = telefone
        dados_pessoais.cep = cep
        dados_pessoais.endereco = endereco
        dados_pessoais.numero_casa = numero_casa
        dados_pessoais.bairro = bairro
        dados_pessoais.cidade = cidade

        # Salvar as alterações
        dados_pessoais.save()
        mensagem_sucesso = "Alterações salvas com sucesso!"
        # Redirecionar para uma página de confirmação ou outra página desejada
        return render(request, 'edita_dados_pessoais.html', {'dados': dados_pessoais, 'mensagem_sucesso': mensagem_sucesso})

    return render(request, 'edita_dados_pessoais.html', {'dados': dados_pessoais})
