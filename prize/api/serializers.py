from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    SerializerMethodField,
    CharField
)
from datetime import date, timedelta

from prize.models import Prizes, UserRedeemedPrizes, PrizeCategory


# Serializer para fornecer as categorias de prêmios em um endpoint
class PrizeCategorySerializer(ModelSerializer):
    class Meta:
        model = PrizeCategory
        fields = ("name", "id")


# Serializer dos prêmios
class PrizesSerializer(ModelSerializer):
    # Geração de um novo campo ao serializer que não está diretamente presente no modelo Prizes.
    generated_by_company_name = SerializerMethodField()

    class Meta:
        model = Prizes
        fields = (
            "name",
            "id",
            "description",
            "cost_in_points",
            "category",
            "generated_by_company_name",
            "logo",
            "times_to_be_used",
            "expiry_date",
            "disabled",
            "generated_by_slug",
        )

    # Fornece o valor para o campo generated_by_company_name.
    def get_generated_by_company_name(self, obj):
        return obj.generated_by.partner_company_name

    # Valida a data de expiração para a criação de um prêmio por parte de um parceiro
    # Um prêmio deve possuir no minimo uma semana de validade e não pode criar no dia atual ou em um dia passado
    def validate_expiry_date(self, value):
        today = date.today()
        one_week_from_today = today + timedelta(weeks=1)

        if value <= today:
            raise ValidationError("The expiry date can't be today or in the past.")

        if value <= one_week_from_today:
            raise ValidationError(
                "O prêmio necessita possuir no mínimo uma semana de validade."
            )
        return value


# Seriliazer para o resgate de prêmios dos usuários
class UserRedeemedPrizesSerializer(ModelSerializer):
    class Meta:
        model = UserRedeemedPrizes
        fields = (
            "prize",
            "is_used",
        )

    # Quando realizarmos um GET dos prêmios resgatados do usuário,
    # Será passado o campo "prizes" serializado
    # para os demais métodos será utilizado o campo prizes apenas com o ID
    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Verifica se é um metodo GET
        if self.context["request"].method == "GET":
            data["prize"] = PrizesSerializer(instance.prize).data
        return data


# Serializa o QR Code (link da API) de um prêmio resgatado pelo usuário
class UserRedeemedPrizesQrCodeSerializer(ModelSerializer):
    class Meta:
        model = UserRedeemedPrizes
        fields = ("qr_code",)


# Serializer para o resgate de prêmios por parte da empresa Parceira.
# Aqui, a empresa irá ler o QR Code que o usuário possui
# A implementação do sistema acaba por aqui, partindo da empresa fornecer
# Corretamente o desconto em seu estabelecimento
class PartnerRedeemPrizeSerializer(ModelSerializer):
    code = CharField(max_length=20)
    class Meta:
        model = UserRedeemedPrizes
        fields = ("code",)

    # Aqui validamos se o código fornecido pelo parceiro no momento da leitura é válido
    # Ou seja, se existe uma instância dele
    def validate_code(self, value):
        try:
            UserRedeemedPrizes.objects.get(code=value)
        except UserRedeemedPrizes.DoesNotExist:
            raise ValidationError("Código Fornecido Inválido")

        return value
