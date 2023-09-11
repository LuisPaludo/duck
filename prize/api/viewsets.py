from sqlite3 import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError
from django.utils import timezone

from prize.models import Prizes, UserRedeemedPrizes, PrizeCategory
from .serializers import (
    PrizesSerializer,
    UserRedeemedPrizesSerializer,
    UserRedeemedPrizesQrCodeSerializer,
    PrizeCategorySerializer,
    PartnerRedeemPrizeSerializer,
)
from user_data.models import History


# View acessada apenas por usuários autenticados
# No get é fornecido todos os prêmios disponíveis
# Para post, apenas usuários parceiros podem chamar o método
class PrizesViewSet(viewsets.ModelViewSet):
    queryset = Prizes.objects.all()
    serializer_class = PrizesSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Verificar se o usuário é uma empresa parceira
        if not request.user.is_partner:
            return Response(
                {"detail": "Apenas parceiros podem criar prêmios."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)

    # Alguns campos não são fornecidos no EndPoint e são tratados como padrão
    # O campo generated_by é associado ao parceiro que criou o prêmio
    # Justamente, a logo do prêmio é a logo da empresa
    # O campo generated_by_slug, permite de uma maneira mais fácil o usuário (ou parceiro)
    # acessar as informações referentes a empres que criou o prêmio
    def perform_create(self, serializer):
        # Associar o "generated_by" ao usuário que está fazendo a requisição
        serializer.save(
            generated_by=self.request.user,
            logo=self.request.user.profile_photo,
            generated_by_slug=self.request.user.partner_company_name_slug,
        )


# View para retornar todas as categorias de prêmio disponíveis
# No front End servirá para filtrar os prêmios e melhorar a interface
class PrizeCategoryViewSet(viewsets.ModelViewSet):
    queryset = PrizeCategory.objects.all()
    serializer_class = PrizeCategorySerializer
    permission_classes = [IsAuthenticated]

# View para fornecer para um parceiro apenas os prêmios criados por ele mesmo
class PartnerCreatedPrizesViewSet(viewsets.ModelViewSet):
    queryset = Prizes.objects.all()
    serializer_class = PrizesSerializer
    permission_classes = [IsAuthenticated]

    # Aqui verificamos se o usuário é parceiro, se sim, filtramos Prizes e buscamos os
    # prêmios gerados por ele
    def get_queryset(self):
        if self.request.user.is_partner:
            return Prizes.objects.filter(generated_by=self.request.user)
        return Prizes.objects.none()


# View para o usuário resgatar prêmios e visualizar os seus prêmios
class UserRedeemedPrizesViewSet(viewsets.ModelViewSet):
    queryset = UserRedeemedPrizes.objects.all()
    serializer_class = UserRedeemedPrizesSerializer
    permission_classes = [IsAuthenticated]

    # Retorna os prêmios do usuário autenticado
    def get_queryset(self):
        return UserRedeemedPrizes.objects.filter(user=self.request.user)

    # Método para a obtenção de um novo prêmio por parte do usuário
    def create(self, request, *args, **kwargs):
        # Verificar se o usuário é uma empresa parceira, se sim, retorna uma mensagem
        # Informando que apenas usuários podem resgatar Prêmios
        if self.request.user.is_partner:
            return Response(
                {"detail": "Apenas Usuários Podem Resgatar Prêmios."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Da requisição, obtêm o ID do prêmio a ser resgatado
        prize_id = request.data.get("prize")

        # Tenta buscar um prêmio com o id obtido
        # Acaba sendo dificil cair na exceção dessa tentativa, porém está aqui como um backup
        try:
            prize = Prizes.objects.get(id=prize_id)
        except Prizes.DoesNotExist:
            return Response(
                {"detail": "Prêmio Não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

        # Verifica se ainda restam unidades do prêmio para serem resgatadas
        if prize.times_to_be_used == 0:
            return Response(
                {"detail": "Não restam mais unidades desse prêmio."},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        # Por fim, verifica se o prêmio possui o status de desabilitado
        # Um prêmio pode ser desabilitado pela empresa parceira, impedindo que novos usuários adquiram aquele prêmio
        # Foi adicionada essa opção pois não existe a exclusão de um prêmio, uma vez que o usuário trocou seus pontos
        # o prêmio é dele, o máximo que uma empresa pode fazer é impedir que novas instâncias do prêmio sejam resgatas
        if prize.disabled:
            return Response(
                {"detail": "Prêmio Desabilitado."}, status=status.HTTP_423_LOCKED
            )

        # Atualiza a quantia de vezes que um prêmio foi resgatado
        prize.times_used += 1
        # Atualiza quantas unidades do prêmio restam para serem resgatadas
        prize.times_to_be_used = prize.times_to_be_used - 1

        # Se um prêmio atingiu seu limite de unidades, é então desabilitado
        if prize.times_to_be_used == 0:
            prize.disabled = True

        # Tenta adquirir os pontos totais do usuário que está resgatando o prêmio
        # os pontos totais ficam sempre armazenados na última instância da model History
        # Como a model possui um campo Date, podemos filtrar para encontrar o total de pontos atuais do usuário
        try:
            last_total_points = (
                History.objects.filter(user=self.request.user)
                .latest("date")
                .total_points
            )
        # Caso não exista uma entrada é associado 0 a total_points
        except History.DoesNotExist:
            last_total_points = 0

        # Se a última pontuação do usuário for menor que o custo do Prêmio retorna um erro
        if last_total_points < prize.cost_in_points:
            return Response(
                {"Usuário não possui pontos suficientes"},
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )

        # Aqui está involto de um try except por causa da particularidade do campo
        # unique together definido na model. Caso um usuário tente resgatar o mesmo cupom sendo que ele já possui uma
        # instância, ao invés de um erro normal temos um IntegrityError
        try:
            response = super().create(request, *args, **kwargs)

            # Criar uma instância de History, para armazenar a nova pontuação e a ação do usuário
            history = History(
                user=self.request.user,
                points=-prize.cost_in_points,
                total_points=last_total_points - prize.cost_in_points,
                description=f"Prêmio Resgatado -> {prize.name}",
            )
            history.save()
            prize.save()
            return response

        except IntegrityError:
            return Response(
                {"detail": "Este prêmio já foi resgatado pelo usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # O campo ID do user não é fornecido no post, ele é inserido com esse método
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


# O usuário nem sempre possui seu QR Code, ele apenas pode observá-lo fazendo uma chamada para essa view.
# a chamada é feita pelo endpoint '/qr-code/?prize=(ID do prize aqui)
class UserRedeemedPrizesQrCodeViewSet(viewsets.ModelViewSet):
    queryset = UserRedeemedPrizes.objects.all()
    serializer_class = UserRedeemedPrizesQrCodeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Recupera o prize da URL
        prize_filter = self.request.query_params.get("prize", None)

        # Se não for fornecido nenhum ID, retorna um objeto vazio
        if prize_filter is None or prize_filter == "":
            return UserRedeemedPrizes.objects.none()

        # Recupera todas os prêmios resgatados pelo usuário
        user_reddemed_prizes = UserRedeemedPrizes.objects.filter(user=self.request.user)

        # Recupera apenas a instância do prêmio fornecida na URL (ID), desse prêmio, será retornado para o usuário
        # apenas o link do QR Code
        return user_reddemed_prizes.filter(prize=prize_filter)


# View para checar o código QR fornecido pelo usuário ao representante da empresa
# Essa view aceita apenas o método post, o objetivo dela é dar uma camada de segurança a empresa
# Quando for ler um QR Code do usuário. Ele pode conferir as informações do Prêmio e do usuário para validar
# o prêmio
class PartnerCheckRedeemPrizeViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerRedeemPrizeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = [
        "post",
    ]

    # Na chamada do método post
    def create(self, request):
        # Cria uma instância para obter a validação realizada no serializer
        serializer = self.serializer_class(data=request.data)

        # Aqui retornaria inválido caso o código fornecido pelo usuário fosse inválido
        if serializer.is_valid():
            # se existe um código, salvamos ele em uma váriavel
            code = serializer.validated_data["code"]
            # Obtemos a instância do prêmio resgatado pelo usuário através do código
            redeemed_prize = UserRedeemedPrizes.objects.get(code=code)

            # Verificamos se o prêmio já foi usado anteriormente, caso positivo, retornamos um erro
            if redeemed_prize.is_used:
                return Response(
                    {"detail": "Este prêmio já foi resgatado"},
                    status=status.HTTP_409_CONFLICT,
                )

            # Verificamos se o prêmio foi criado por uma empresa diferente que o está resgatando nesse momento
            # Caso positovo, retornamos um erro
            if redeemed_prize.prize.generated_by != request.user:
                return Response(
                    {"detail": "Este prêmio não foi gerado por essa empresa."},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

            # Verificamos se a data de validade do prêmio já passou, caso positivo retornamos um erro
            if redeemed_prize.prize.expiry_date < timezone.now().date():
                return Response(
                    {"detail": "Prêmio expirado"},
                    status=status.HTTP_410_GONE,
                )

            # Aqui montamos uma resposta personalizada, fornecendo informações sobre o usuário e o prêmio
            # As informações do prêmio são obtidas com o serializer do mesmo
            response_data = {
                "username": redeemed_prize.user.username,
                "first_name": redeemed_prize.user.first_name,
                "last_name": redeemed_prize.user.last_name,
                "cpf": redeemed_prize.user.cpf,
                "prize": PrizesSerializer(redeemed_prize.prize).data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View para efetuar a ação de resgate de um prêmio por parte da empresa
class PartnerRedeemPrizeViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerRedeemPrizeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = [
        "post",
    ]

    # Na chamada do método Post
    def create(self, request):
        # Criamos uma instância novamente para validar o código fornecido
        serializer = self.serializer_class(data=request.data)

        # Se for válido
        if serializer.is_valid():
            # Extraímos o código
            code = serializer.validated_data["code"]
            # Obtemos o prêmio resgatado
            redeemed_prize = UserRedeemedPrizes.objects.get(code=code)

            # Obtemos o valor de pontos totais atuais do usuário (necessário para registrar no histórico dele)
            last_total_points = (
                History.objects.filter(user=redeemed_prize.user)
                .latest("date")
                .total_points
            )

            # Criamos uma instância no histórico do usuário registrândo a ação de utilização do prêmio
            history = History(
                user=redeemed_prize.user,
                points=0,
                total_points=last_total_points,
                description=f"Prêmio utilizado -> {redeemed_prize.prize.name}",
            )
            history.save()

            # Identificamos que o prêmio foi utilizado
            redeemed_prize.is_used = True
            redeemed_prize.save()

            response_data = {"message": "Prize redeemed successfully."}

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
