from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from datetime import timedelta
from django.utils import timezone

from user_data.models import History, CustomUser
from .serializers import (
    CustomUserSerializer,
    HistorySerializer,
)

# ViewSet responsável pela criação de entradas no histórico do usuário.
# Aceita métodos como GET que retorna para o usuário todas as informações
# E post que permite uma nova entrada
class HistoryViewSet(ModelViewSet):
    serializer_class = HistorySerializer
    http_method_names = ["get", "post"]
    # Somente acessada por usuários autenticados
    permission_classes = [IsAuthenticated]

    # Quando recebe uma chamada get, retorna as informações especificas do usuário autenticado
    # Um usuário não pode acessar as informações de outro usuário
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return History.objects.filter(user=self.request.user)
        # Retorna um queryset vazio quando o usuário não está autenticado.
        return History.objects.none()

    # O método create deve funcionar da seguinte forma:
    # - Um usuário não pode registrar uma nova entrada (que valha pontos) em menos de 5 minutos
    # - Caso o usuário atinja o limite de pontos diários, os pontos devem ser limitados
    # por exemplo, se ele tinha 100 de limite e capturou um ponto de 150, 50 pontos serão "jogados fora"
    # e serão acrescentados apenas 100 pontos na sua conta
    def create(self, request, *args, **kwargs):
        user = request.user # recupera o usuário da request
        five_minutes_ago = timezone.now() - timedelta(minutes=5) # Calcula um intervalo de tempo de 5 minutos a partir do tempo atual

        if self.request.user.is_partner: # Se o usuário é "parceiro", retorna 403, pois parceiros não podem acumular pontos
            return Response(
                {"Parceiros não podem resgatar pontos"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        # Verificar se uma entrada foi criada nos últimos 5 minutos filtrando a model history do usuário autenticado
        recent_entry = History.objects.filter(
            user=user, date__gte=five_minutes_ago
        ).first()        

        if recent_entry and recent_entry.points != "0": # Se existir uma entrada recente, e, caso exista, testar se a pontuação não é nula
            # Essa lógica permite que, após o limite diário o usuário receba apenas a mensagem de limite diário
            # Resgatar prêmiso com empresas parceiras não resulte em uma limitação para ganhar mais pontos
            return Response(
                {"Você só pode criar uma entrada a cada 5 minutos."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        # Salva a reposta e cria uma instância
        response = super().create(request, *args, **kwargs)

        # Verificar se os pontos foram ajustados no serializer
        if response.status_code == status.HTTP_201_CREATED:
            # recupera os pontos da response, caso não existam, é atribuido 0
            added_points = response.data.get("points", 0)
            # Se os pontos adicionados, obtidos na response, forem menores que os pontos da request, significa que foram ajustados
            if added_points < request.data.get("points"):
                # Fornece a mensagem para o usuário
                response.data[
                    "message"
                ] = "Os pontos foram ajustados com base no limite diário."

        return response

    # Quando a função Create for chamada nessa view, ajusta para que o usuário seja o usuário da request
    # isso é feito para que o usuário não precise ser fornecido na chamada
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# View para atribuir uma página ao serviço de verificação do email
class CustomVerifyEmailView(CreateAPIView):
    def get_queryset(self):
        return

# View que tem como intuito apresentar as informações de usuários parceiros para os outros usuários (normais e parceiros)
class PartnerDetailsViewSet(ModelViewSet):
    # Filtro apenas os usuários parceiros no meu banco de dados
    queryset = CustomUser.objects.filter(is_partner=True)
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    # Ao invpes de buscar o usuário pela ID, buscará pelo campo "partner_company_name_slug", que será fornecido na URL
    lookup_field = "partner_company_name_slug"

    # A função retrieve é basicamente uma ação para buscar um único registro do banco de dados baseado em um identificador
    # nesse caso "partner_company_name_slug
    def retrieve(self, request, *args, **kwargs):
        # tenta obter um parceiro através do argumento fornecido na chamada, returna um erro caso não encontre
        try:
            partner = self.queryset.get(partner_company_name_slug=kwargs["partner_company_name_slug"])
        except CustomUser.DoesNotExist:
            raise NotFound("Não existe um parceiro com o nome da empresa fornecido")

        # Se encontrou um usuário, mas ele não é parceiro, retorna um erro
        # (Acaba sendo redundante essas linhas, visto que já foi verificado anteriormente)
        if not partner.is_partner:
            raise PermissionDenied(
                "Você só pode acessar detalhes de usuários que são parceiros"
            )

        # Se encontrou um parceiro, retorna as seguintes informações apenas
        return Response(
            {
                "partner_company_name": partner.partner_company_name,
                "partner_email_contact": partner.partner_email_contact,
                "partner_number_contact": partner.partner_number_contact,
                "address_street": partner.address_street,
                "address_city": partner.address_city,
                "profile_photo": partner.profile_photo.url,
                "cep": partner.cep,
                "partner_company_description": partner.partner_company_description,
            },
            status=status.HTTP_200_OK,
        )
