from django.db import models
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

import random, string

from user_data.models import CustomUser
from user_data.models import validate_image_size


# Função para gerar códigos de 20 caracteres aleatórios. Isso permite os pontos turísticos e os prêmios
# Possuírem códigos únicos associados
def generate_random_code():
    # Escolhe 20 caracteres aleatoriamente do conjunto de letras maiúsculas e dígitos
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=20))


# Model para categorizar os prêmios: No momento foi pensado em Brindes e Descontos
class PrizeCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Model para os prêmios a serem resgatados pelos usuários
class Prizes(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    generated_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="generated_prizes"
    )
    generated_by_slug = models.SlugField(blank=True, null=True)
    times_to_be_used = models.IntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(3000)]
    )
    times_used = models.IntegerField(default=0)
    cost_in_points = models.IntegerField(
        default=0, validators=[MinValueValidator(100), MaxValueValidator(1000)]
    )
    category = models.ForeignKey(
        PrizeCategory, on_delete=models.SET_NULL, null=True, related_name="prizes"
    )
    logo = models.ImageField(
        upload_to="logos",
        null=True,
        blank=True,
        default="users_photos/default.png",
        validators=[validate_image_size],
        max_length=500,
    )
    expiry_date = models.DateField()
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Model para os prêmios resgatados dos usuários
class UserRedeemedPrizes(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="redeemed_prizes"
    )
    prize = models.ForeignKey(
        Prizes, on_delete=models.CASCADE, related_name="claimed_by"
    )
    redeemed_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    qr_code = models.URLField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        # Esse campo permite que apenas uma instância de cada prêmio possa ser resgatada por cada usuário
        unique_together = ("user", "prize")

    def save(self, *args, **kwargs):
        # O prêmio originalmente é resgatado e não é fornecido um código para ele
        # O Código é gerado automaticamente por esse método
        if not self.code:
            self.code = generate_random_code()
            while UserRedeemedPrizes.objects.filter(code=self.code).exists():
                self.code = generate_random_code()

        # Depois de gerado o código, é criado o QR Code com o auxílio de uma API
        self.qr_code = (
            f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={self.code}"
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} -> {self.prize}"
