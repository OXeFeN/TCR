from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrace proběhla úspěšně. Nyní se můžete přihlásit.')
            return redirect('login')  # Změňte 'login' na vámi požadovanou URL pro přihlášení
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})
