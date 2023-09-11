from enum import unique
from os import name
from django.db import models
from django.core.validators import MinValueValidator

from prize.models import generate_random_code
from user_data.models import validate_image_size
from django.utils.text import slugify


# Model para armazenar os pontos turísticos da cidade
# Aqui funcionará como um ponto "mãe". Por exemplo,
# Parque do alvorecer será um objeto dessa model, e, diversos pontos turísticos localizados no parque
# Estarão referenciados a essa model aqui. Essa model também irá ser impressa em uma página no Front End,e permitindo que o usuário
# Facilmente acesse as informações e conheça o local para então visitar e buscar QR Codes na região
class Location(models.Model):
    name = models.CharField(max_length=255)
    resume = models.TextField()
    description = models.TextField()
    review_link = models.URLField(max_length=255, default="")
    map_link = models.URLField(max_length=255, default="")
    coordinates_lat = models.CharField(max_length=255, default="")
    coordinates_long = models.CharField(max_length=255, default="")
    slug_field = models.SlugField(default="", blank=True, null=True)
    photo_1 = models.ImageField(
        upload_to="Locations",
        null=True,
        blank=True,
        validators=[validate_image_size],
        max_length=500,
    )
    photo_2 = models.ImageField(
        upload_to="Locations",
        null=True,
        blank=True,
        validators=[validate_image_size],
        max_length=500,
    )
    photo_3 = models.ImageField(
        upload_to="Locations",
        null=True,
        blank=True,
        validators=[validate_image_size],
        max_length=500,
    )
    photo_4 = models.ImageField(
        upload_to="Locations",
        null=True,
        blank=True,
        validators=[validate_image_size],
        max_length=500,
    )

    def __str__(self) -> str:
        return self.name

    # Quando a model é salva, verifica se a variável name não é nula e não é apenas um campo vazio
    # Em caso da variável existir, cria o campo de slug para ajudar na navegação
    def save(self, *args, **kwargs):
        if self.name and not self.name.isspace():
            self.slug_field = slugify(self.name)

        super(Location, self).save(*args, **kwargs)


# Model que representa os pontos turísticos. Aqui estarão salvas as informações referentes a
# lugares especificos em pato branco. Por exemplo, aqui pode conter o pato platinado que tem no parque do alvorecer
# (Ficou um pouco confuso Locations e TouristAttraction, porém bem explicado acho que vai embora kkk)
# Essa model ficará apenas acessível ao usuário quando ele resgatar um QR Code. O fluxo seria o seguinte:
# Usuário Lê o QR Code em uma atração turistica em pato branco, se der positivo, será feita uma chamada e como resposta
# Serão passadas as informações referentes ao pontos turistico que ele leu o QR Code
class TouristAttraction(models.Model):
    class Meta:
        verbose_name_plural = "Tourist Attractions"

    name = models.CharField(max_length=255)
    resume = models.TextField()
    description = models.TextField()
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    qr_code = models.CharField(max_length=255, unique=True, blank=True, null=True)
    location = models.ForeignKey(
        Location, related_name="location_points", on_delete=models.SET_NULL, null=True
    )
    coordinates_lat = models.CharField(max_length=255, default="")
    coordinates_long = models.CharField(max_length=255, default="")
    points = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    photo = models.ImageField(
        upload_to="Locations/Touristic_Points",
        null=True,
        blank=True,
        validators=[validate_image_size],
        max_length=500,
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.location}) -> Points: {self.points}"

    # Quando um novo objeto é salvo associa um código aleatório ao campo "code", em seguida
    # Chama a API para criar um QR Code
    def save(self, *args, **kwargs):
        # Apenas gera um código se não existe um código
        if not self.code:
            self.code = generate_random_code()
            # Faz um loop para impedir que existam códigos repetidos
            while TouristAttraction.objects.filter(code=self.code).exists():
                self.code = generate_random_code()

        self.qr_code = (
            f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={self.code}"
        )
        super().save(*args, **kwargs)
