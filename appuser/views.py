from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from .models import Appuser

def Register(request):
    # Se l'utente è già loggato lo reindirizzo alla home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Salva l'utente
            print("Registrazione avvenuta con successo!")
            return redirect('login')  # Reindirizza alla pagina di login
        else:
            # Controllo se ci sono dei messaggi di errore predefiniti di Django
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = RegistrationForm()

    return render(request, 'appuser/register/register.html', {'form': form})


def Login(request):
    # Se l'utente è già loggato lo reindirizzo alla home
    if request.user.is_authenticated:
        return redirect('home')
    
    form = LoginForm(request.POST or None) 
    message = ''

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            utente = authenticate(username=username, password=password) # Se l'utente viene autenticato viene restituito un oggetto Utente, altrimenti None
            if utente is not None:
                login(request, utente)  # Effettua il login
                return redirect('home')
            else:
                message = 'Credenziali non valide'
        else:
            message = 'Errore nel login'
    return render(request, 'appuser/login/login.html', {'form': form, 'message': message})

def Logout(request):
    logout(request)
    return redirect('home')