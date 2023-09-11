from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db.models import Sum
from django.utils import timezone

from user_data.models import CustomUser, History

# Serializer para o usuário
# Retorna os seguintes campos e, a informação dele ser parceiro ou não é apenas para leitura
# Novos parceiros podem ser gerados apenas pelo administrador do sistema
# Não existe nenhuma outra forma de registrar novos parceiros
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "cep",
            "cpf",
            "cnpj",
            "address_street",
            "address_state",
            "address_city",
            "profile_photo",
            "birth_date",
            "is_partner",
            "partner_company_name",
            "partner_email_contact",
            "partner_number_contact",
            "partner_company_description",
            "partner_company_name_slug",
        )
        read_only_fields = ("is_partner",)


# Serializer para o histórico do usuário
class HistorySerializer(serializers.ModelSerializer):
    # Total points é apenas para leitura, pois ele é calculado no servidor
    class Meta:
        model = History
        fields = ("date", "points", "total_points", "description")
        read_only_fields = ("total_points",)  # tornando 'total_points' somente leitura

    # Na chamada de create uma nova entrada
    def create(self, validated_data):
        # Recupera o usuário da requisição
        user = self.context["request"].user

        # Verificar a soma total de pontos que o usuário obteve hoje
        today_min = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_max = timezone.now().replace(
            hour=23, minute=59, second=59, microsecond=999999
        )
        # Filtra a model histpry com o usuário resgatado e o intervalo de tempo criado. Faz um somatório dos pontos encontrados
        total_points_today = (
            History.objects.filter(
                user=user, date__range=(today_min, today_max)
            ).aggregate(total_points=Sum("points"))["total_points"]
            or 0
        )

        daily_limit = 700 # Limite diário de pontos
        points = validated_data.get("points", 0) # Recupera os pontos fornecidos na requisição
        points_left_for_today = daily_limit - total_points_today #  Define quantos pontos restam para o usuário resgatar hoje

        # Verifica se há pontos a serem resgatados ainda
        if points_left_for_today < points:
            # Define um novo valor para os pontos, sobreescrevendo o valor fornecido na chamada
            validated_data["points"] = points_left_for_today

        # Calcula o total points do usuário fazendo um somatório de todas as entradas de points
        previous_total_points = (
            user.user_history.aggregate(total_points=Sum("points"))["total_points"] or 0
        )
        # Sobreescreve o valor de total_points somando o valor obtido no somatório com os novos pontos a serem adicionados
        validated_data["total_points"] = (
            previous_total_points + validated_data["points"]
        )

        return History.objects.create(**validated_data)

# Serializer para registrar novos usuários (Configurado no settings.py, linha 190)
class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    cep = serializers.CharField(max_length=13)
    cpf = serializers.CharField(max_length=20)
    address_street = serializers.CharField(max_length=255)
    address_state = serializers.CharField(max_length=2)
    address_city = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    profile_photo = serializers.ImageField(
        required=False, allow_null=True
    )
    birth_date = serializers.DateField(required=False)
    is_terms_accepted = serializers.BooleanField()

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
            "cep",
            "cpf",
            "address_street",
            "address_state",
            "address_city",
            "profile_photo",
            "birth_date",
            "is_terms_accepted",
        )

    #  Valida se o usuário aceitou os termos propostos no cadastro
    def validate_accepted_terms(self, value):
        # Senão Aceitou, retorna um erro
        if value is not True:
            raise serializers.ValidationError("You must accept the terms to register.")
        return value

    # Este método é usado para personalizar o processo de registro. Ele pega os dados validados e 
    # os atribui aos atributos do objeto de usuário correspondente e, em seguida, salva esse objeto no banco de dados.
    def custom_signup(self, request, user):
        user.cep = self.validated_data.get("cep", "")
        user.first_name = self.validated_data.get("first_name", "")
        user.last_name = self.validated_data.get("last_name", "")
        user.cpf = self.validated_data.get("cpf", "")
        user.address_street = self.validated_data.get("address_street", "")
        user.address_state = self.validated_data.get("address_state", "")
        user.address_city = self.validated_data.get("address_city", "")
        user.email = self.validated_data.get("email", "")
        user.profile_photo = self.validated_data.get("profile_photo", None)
        user.birth_date = self.validated_data.get("birth_date", None)
        user.is_terms_accepted = self.validated_data.get("is_terms_accepted", None)
        user.save()

    # Este método é usado para obter os dados limpos (ou validados) de todos os campos definidos no serializer. Ele se 
    # baseia na implementação get_cleaned_data da classe base e, em seguida, adiciona os campos adicionais definidos neste serializer personalizado.
    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            **super().get_cleaned_data(),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "cep": self.validated_data.get("cep", ""),
            "cpf": self.validated_data.get("cpf", ""),
            "address_street": self.validated_data.get("address_street", ""),
            "address_state": self.validated_data.get("address_state", ""),
            "address_city": self.validated_data.get("address_city", ""),
            "birth_date": self.validated_data.get("birth_date", ""),
            "email": self.validated_data.get("email", ""),
            "profile_photo": self.validated_data.get("profile_photo", ""),
            "is_terms_accepted": self.validated_data.get("is_terms_accepted", ""),
        }
