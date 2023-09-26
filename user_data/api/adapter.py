from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_username
from dj_rest_auth.forms import AllAuthPasswordResetForm, default_token_generator
from duck.settings import URL_FRONTEND

# Adaptador personalizado para a conta que estende o adaptador padrão do Allauth.
class CustomAccountAdapter(DefaultAccountAdapter):
    # Gera a URL para confirmação de email usando o frontend personalizado.
    def get_email_confirmation_url(self, request, emailconfirmation):
        return f'{URL_FRONTEND}/verificacao-email/{emailconfirmation.key}'

# Função para gerar URL personalizada para redefinição de senha.
def custom_url_generator(request, user, temp_key):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = temp_key
    reset_url = f'{URL_FRONTEND}login/reset/confirmar/{uidb64}/{token}'
    return reset_url

# Formulário personalizado para redefinição de senha que estende o formulário padrão do Allauth.
class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):

    # Salva o formulário e envia o email de redefinição de senha com a URL personalizada.
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # Use a função custom_url_generator para obter a URL personalizada.
            url = custom_url_generator(request, user, temp_key)

            context = {
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'request': request,
            }
            if (
                allauth_account_settings.AUTHENTICATION_METHOD
                != allauth_account_settings.AuthenticationMethod.EMAIL
            ):
                context['username'] = user_username(user)

            # Envia o email de redefinição de senha.
            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context
            )
        return self.cleaned_data['email']