from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # načte váš CustomUser
        fields = ('username', 'email')  # případně přidejte další pole, pokud potřebujete
