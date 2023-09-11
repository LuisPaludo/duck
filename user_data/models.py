from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify


# Função auxiliar para validar as imagens fornecidas pelos usuários.
# A função verifica se o tamanho da imagem não supera 2MB, para evitar
# a superlotação do banco de dados.
def validate_image_size(value):
    imagesize = value.size

    if imagesize > 2097152:
        raise ValidationError("Tamanho Máximo permitido: 2MB")
    else:
        return value


# Model personalizadad para o usuário
# A model servirá tanto para usuários convencionais quanto para usuários parceiros
class CustomUser(AbstractUser):
    class Meta:
        verbose_name_plural = "Users"

    cep = models.CharField(max_length=13)
    cpf = models.CharField(max_length=20, blank=True, null=True)
    cnpj = models.CharField(max_length=20, blank=True, null=True, unique=True)
    address_street = models.CharField(max_length=255)
    address_state = models.CharField(max_length=2)
    address_city = models.CharField(max_length=255)
    email = models.EmailField()
    profile_photo = models.ImageField(
        upload_to="users_photos",
        null=True,
        blank=True,
        default="users_photos/default.png",
        validators=[validate_image_size],
        max_length=500,
    )
    birth_date = models.DateField(null=True, blank=True)
    is_terms_accepted = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    partner_company_name = models.CharField(
        max_length=50, blank=True, null=True, unique=True
    )
    partner_company_name_slug = models.SlugField(unique=True, blank=True, null=True)
    partner_email_contact = models.EmailField(blank=True, null=True)
    partner_number_contact = models.IntegerField(blank=True, null=True)
    partner_company_description = models.TextField(blank=True, null=True)

    # Muda a forma como o usuário é apresentado
    def __str__(self) -> str:
        return f"{self.username}"

    # Quando a model é salva, verifica se a variável partner_company_name não é nula e não é apenas um campo vazio
    # Em caso da variável existir, cria o campo de slug para ajudar na navegação
    def save(self, *args, **kwargs):
        if self.partner_company_name and not self.partner_company_name.isspace():
            self.partner_company_name_slug = slugify(self.partner_company_name)

        super(CustomUser, self).save(*args, **kwargs)


# Model para armazenar as ações do usuário. Não é utilizada para o caso do usuário ser um parceiro.
# Aqui ficam salvas as informações como obtenção de pontos, resgate e compra de prêmios.
class History(models.Model):
    class Meta:
        verbose_name_plural = "Users History"

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_history"
    )
    date = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)
    total_points = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.CharField(max_length=255)

    # Muda a forma como a model é impressa
    def __str__(self) -> str:
        return f"{self.user.username}"
