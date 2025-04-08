from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, get_user_model
from .models import CustomUser



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrace proběhla úspěšně a jste nyní přihlášeni.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Zkontrolujte formulář – některá pole nejsou správně vyplněna.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # pojmenuj si podle své URL
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

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

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_edit_user(request, user_id):
    target_user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Uživatel {target_user.username} byl úspěšně upraven.")
            return redirect('user_management')
        else:
            messages.error(request, "Formulář obsahuje chyby. Zkontrolujte prosím všechna pole.")
    else:
        form = CustomUserForm(instance=target_user)

    return render(request, 'user_edit_profile.html', {
        'form': form,
        'target_user': target_user
    })