from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, get_user_model

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

User = get_user_model()

@staff_member_required
def user_management(request):
    if request.method == 'POST':
        for user_id in request.POST.getlist('user_ids'):
            try:
                user = User.objects.get(pk=user_id)
                checkbox_name = f'paid_{user.id}'
                user.membership_paid = checkbox_name in request.POST
                user.save()
            except User.DoesNotExist:
                pass  # volitelně logovat

        return redirect('user_management')

    staff_users = User.objects.filter(is_staff=True)
    regular_users = User.objects.filter(is_staff=False)

    return render(request, 'users/user_management.html', {
        'staff_users': staff_users,
        'regular_users': regular_users,
    })

@staff_member_required
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        # Zamezíme, aby uživatel mohl smazat sám sebe
        if user != request.user and not user.is_superuser:
            user.delete()
    return redirect('user_management')


@staff_member_required
def delete_users_bulk(request):
    if request.method == 'POST':
        ids = request.POST.getlist('user_ids_to_delete')
        for uid in ids:
            try:
                user = User.objects.get(pk=uid)
                # Nesmíme smazat sami sebe nebo superuživatele
                if user != request.user and not user.is_superuser:
                    user.delete()
            except User.DoesNotExist:
                pass
    return redirect('user_management')