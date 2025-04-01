from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Uloží nového uživatele
            # Získání údajů pro autentizaci
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # Autentizace uživatele
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)  # Přihlášení uživatele
                messages.success(request, 'Registrace proběhla úspěšně a jste nyní přihlášeni.')
                return redirect('dashboard')  # Přesměrování na stránku po přihlášení (např. dashboard)
            else:
                messages.error(request, 'Došlo k chybě při autentizaci.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})

@login_required
def dashboard(request):
    context = {
        'user_full_name': request.user.get_full_name() or request.user.username,
        # přidejte další data dle potřeby
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile_view(request):
    return render(request, 'profile.html')