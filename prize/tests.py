from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import force_authenticate
from model_bakery import baker

from .models import PrizeCategory, Prizes, UserRedeemedPrizes
from user_data.models import CustomUser, History
from user_data.api.viewsets import HistoryViewSet

from .api.viewsets import (
    PrizesViewSet,
    PrizeCategoryViewSet,
    PartnerCreatedPrizesViewSet,
    UserRedeemedPrizesViewSet,
    UserRedeemedPrizesQrCodeViewSet,
    PartnerCheckRedeemPrizeViewSet,
    PartnerRedeemPrizeViewSet,
)

prize_mock_data = {
    "name": "Premio 03",
    "description": "Premio Mock data",
    "cost_in_points": "101",
    "category": "1",
    "times_to_be_used": "200",
    "expiry_date": "2023-10-15",
}

prize_mock_data_expired_date = {
    "name": "Premio 03",
    "description": "Premio Mock data",
    "cost_in_points": "101",
    "category": "1",
    "times_to_be_used": "200",
    "expiry_date": "2023-09-15",
}

prize_mock_data_less_than_one_week_date = {
    "name": "Premio 03",
    "description": "Premio Mock data",
    "cost_in_points": "101",
    "category": "1",
    "times_to_be_used": "200",
    "expiry_date": "2023-09-20",
}


class TestPrizes(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_1 = baker.make(CustomUser, cpf="12345678910")
        self.user_1_last_history = baker.make(
            History, user=self.user_1, points=200, total_points=200
        )
        self.user_2 = baker.make(CustomUser)
        self.user_2_last_history = baker.make(
            History, user=self.user_2, points=0, total_points=0
        )
        self.user_partner_1 = baker.make(
            CustomUser, is_partner=True, partner_company_name="Empresa 01"
        )
        self.user_partner_2 = baker.make(
            CustomUser, is_partner=True, partner_company_name="Empresa 02"
        )
        self.category_1 = baker.make(PrizeCategory, name="Categoria 01")
        self.category_2 = baker.make(PrizeCategory, name="Categoria 02")
        self.prize_1 = baker.make(
            Prizes,
            name="Prêmio 01",
            category=self.category_1,
            generated_by=self.user_partner_1,
            times_to_be_used=10,
            disabled=False,
        )
        self.prize_2 = baker.make(
            Prizes,
            name="Prêmio 02",
            category=self.category_2,
            generated_by=self.user_partner_2,
            times_to_be_used=0,
            disabled=False,
        )
        self.prize_3 = baker.make(
            Prizes,
            name="Prêmio 03",
            category=self.category_2,
            generated_by=self.user_partner_2,
            times_to_be_used=10,
            disabled=True,
        )
        self.prize_4 = baker.make(
            Prizes,
            name="Prêmio 04",
            category=self.category_2,
            generated_by=self.user_partner_2,
            times_to_be_used=10,
            disabled=False,
            cost_in_points=100,
        )
        self.prize_5 = baker.make(
            Prizes,
            name="Prêmio 05",
            category=self.category_2,
            generated_by=self.user_partner_2,
            times_to_be_used=10,
            disabled=False,
            cost_in_points=100,
            expiry_date="2023-09-10",
        )
        self.user_1_redeemed_prize_1 = baker.make(
            UserRedeemedPrizes, prize=self.prize_1, user=self.user_1
        )
        self.user_1_redeemed_prize_2 = baker.make(
            UserRedeemedPrizes, prize=self.prize_2, user=self.user_1
        )
        self.user_2_redeemed_prize_1 = baker.make(
            UserRedeemedPrizes, prize=self.prize_1, user=self.user_2
        )
        self.user_2_redeemed_prize_2 = baker.make(
            UserRedeemedPrizes, prize=self.prize_2, user=self.user_2
        )

    # Testa se a listagem de categorias de prêmios está acessível com autenticação
    def test_prize_category_list_auth(self):
        request = self.factory.get("categorias")
        force_authenticate(request, user=self.user_1)
        view = PrizeCategoryViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_200_OK)

    # Testa a criação de um prêmio por um usuário que não é parceiro
    def test_create_prize_not_partner(self):
        request = self.factory.post("premios", prize_mock_data)
        force_authenticate(request, user=self.user_1)
        view = PrizesViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    # Testa a criação bem-sucedida de um prêmio
    def test_create_prize(self):
        request = self.factory.post("premios", prize_mock_data)
        force_authenticate(request, user=self.user_partner_1)
        view = PrizesViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    # Testa a tentativa de criação de um prêmio com data de expiração passada
    def test_create_prize_expired_date(self):
        request = self.factory.post("premios", prize_mock_data_expired_date)
        force_authenticate(request, user=self.user_partner_1)
        view = PrizesViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        expected_message = "A data não pode ser no passado ou o dia atual"
        self.assertIn(expected_message, str(response.data))

    # Testa a tentativa de criação de um prêmio com menos de uma semana de validade
    def test_create_prize_less_than_one_week_date(self):
        request = self.factory.post("premios", prize_mock_data_less_than_one_week_date)
        force_authenticate(request, user=self.user_partner_1)
        view = PrizesViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        expected_message = (
            "O prêmio necessita possuir no mínimo uma semana de validade."
        )
        self.assertIn(expected_message, str(response.data))

    # Testa a listagem de prêmios criados por um parceiro específico
    def test_list_partner_created_prizes(self):
        request = self.factory.get("criados")
        force_authenticate(request, user=self.user_partner_1)
        view = PartnerCreatedPrizesViewSet.as_view({"get": "list"})
        response = view(request)
        for prize in response.data:
            self.assertEqual(
                prize["generated_by_company_name"],
                self.user_partner_1.partner_company_name,
            )
            self.assertNotEqual(
                prize["generated_by_company_name"],
                self.user_partner_2.partner_company_name,
            )

    # Testa a listagem de prêmios resgatados por um usuário
    def test_list_prizes_redeemed_by_user(self):
        request = self.factory.get("resgatar")
        force_authenticate(request, user=self.user_1)
        view = UserRedeemedPrizesViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_200_OK)

    # Testa a tentativa de resgate de um prêmio já resgatado pelo mesmo usuário
    def test_prize_already_redeemed_by_user(self):
        redeem_prize_mock_data = {
            "prize": f"{self.prize_1.pk}",
        }
        request = self.factory.post("resgatar", redeem_prize_mock_data)
        force_authenticate(request, user=self.user_1)
        view = UserRedeemedPrizesViewSet.as_view({"post": "create"})
        response = view(request)
        expected_message = "Este prêmio já foi resgatado pelo usuário."
        self.assertIn(expected_message, str(response.data))

    # Testa a tentativa de resgate de um prêmio por um parceiro (que não deve ser permitido)
    def test_redeem_prize_as_partner(self):
        redeem_prize_mock_data = {
            "prize": f"{self.prize_1.pk}",
        }
        request = self.factory.post("resgatar", redeem_prize_mock_data)
        force_authenticate(request, user=self.user_partner_1)
        view = UserRedeemedPrizesViewSet.as_view({"post": "create"})
        response = view(request)
        expected_message = "Apenas Usuários Podem Resgatar Prêmios."
        self.assertIn(expected_message, str(response.data))

    # Testa o resgate de um prêmio que não possui mais unidades disponíveis
    def test_no_prize_left_to_redeem(self):
        redeem_prize_mock_data = {
            "prize": f"{self.prize_2.pk}",
        }
        request = self.factory.post("resgatar", redeem_prize_mock_data)
        force_authenticate(request, user=self.user_1)
        view = UserRedeemedPrizesViewSet.as_view({"post": "create"})
        response = view(request)
        expected_message = "Não restam mais unidades desse prêmio."
        self.assertIn(expected_message, str(response.data))

    # Testa a tentativa de resgate de um prêmio que está desabilitado
    def test_redeem_prize_disabled(self):
        redeem_prize_mock_data = {
            "prize": f"{self.prize_3.pk}",
        }
        request = self.factory.post("resgatar", redeem_prize_mock_data)
        force_authenticate(request, user=self.user_1)
        view = UserRedeemedPrizesViewSet.as_view({"post": "create"})
        response = view(request)
        expected_message = "Prêmio Desabilitado."
        self.assertIn(expected_message, str(response.data))

    # Testa o resgate de um prêmio e verifica se os pontos do usuário são reduzidos corretamente
    def test_redeem_prize_check_if_points_are_reduced(self):
        redeem_prize_mock_data = {
            "prize": f"{self.prize_4.pk}",
        }
        request = self.factory.post("resgatar", redeem_prize_mock_data)
        force_authenticate(request, user=self.user_1)
        view = UserRedeemedPrizesViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        request = self.factory.get("usuario/historico")
        force_authenticate(request, user=self.user_1)
        view = HistoryViewSet.as_view({"get": "list"})
        response = view(request)
        last_total_points = (
            History.objects.filter(user=self.user_1).latest("date").total_points
        )
        self.assertEqual(
            self.user_1_last_history.total_points - self.prize_4.cost_in_points,
            last_total_points,
        )

    # Testa a tentativa de resgate de um prêmio quando o usuário não tem pontos suficientes
    def test_redeem_prize_not_enough_points(self):
        redeem_prize_mock_data = {
            "prize": f"{self.prize_4.pk}",
        }
        request = self.factory.post("resgatar", redeem_prize_mock_data)
        force_authenticate(request, user=self.user_2)
        view = UserRedeemedPrizesViewSet.as_view({"post": "create"})
        response = view(request)
        expected_message = "Usuário não possui pontos suficientes"
        self.assertIn(expected_message, str(response.data))

    # Testa um parceiro verificando um prêmio resgatado por um usuário
    def test_partner_checking_user_prize(self):
        user_redeemed_prize_mock_data = {
            "code": f"{self.user_1_redeemed_prize_1.code}",
        }
        request = self.factory.post("checar", user_redeemed_prize_mock_data)
        force_authenticate(request, user=self.user_partner_1)
        view = PartnerCheckRedeemPrizeViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_200_OK)

    # Testa um parceiro tentando verificar um prêmio que não foi gerado por sua empresa
    def test_partner_checking_user_prize_not_same_company(self):
        user_redeemed_prize_mock_data = {
            "code": f"{self.user_1_redeemed_prize_1.code}",
        }
        request = self.factory.post("checar", user_redeemed_prize_mock_data)
        force_authenticate(request, user=self.user_partner_2)
        view = PartnerCheckRedeemPrizeViewSet.as_view({"post": "create"})
        response = view(request)
        expected_message = "Este prêmio não foi gerado por essa empresa."
        self.assertIn(expected_message, str(response.data))

    # Testa um parceiro tentando verificar um prêmio já utilizado
    def test_partner_checking_user_prize_already_redeemed(self):
        user_1_redeemed_prize_4 = baker.make(
            UserRedeemedPrizes, prize=self.prize_4, user=self.user_1, is_used=True
        )
        user_redeemed_prize_mock_data = {
            "code": f"{user_1_redeemed_prize_4.code}",
        }
        request = self.factory.post("checar", user_redeemed_prize_mock_data)
        force_authenticate(request, user=self.user_partner_2)
        view = PartnerCheckRedeemPrizeViewSet.as_view({"post": "create"})
        response = view(request)
        expected_message = "Este prêmio já foi resgatado"
        self.assertIn(expected_message, str(response.data))

    # Testa um parceiro tentando verificar um prêmio que já expirou
    def test_partner_checking_user_prize_expired(self):
        user_1_redeemed_prize_5 = baker.make(
            UserRedeemedPrizes, prize=self.prize_5, user=self.user_1, is_used=False
        )
        user_redeemed_prize_mock_data = {
            "code": f"{user_1_redeemed_prize_5.code}",
        }
        request = self.factory.post("checar", user_redeemed_prize_mock_data)
        force_authenticate(request, user=self.user_partner_2)
        view = PartnerCheckRedeemPrizeViewSet.as_view({"post": "create"})
        response = view(request)
        expected_message = "Prêmio expirado"
        self.assertIn(expected_message, str(response.data))

    # Testa um parceiro verificando os detalhes de um prêmio resgatado por um usuário usando um código válido
    def test_partner_checking_user_prize(self):
        user_redeemed_prize_mock_data = {
            "code": f"{self.user_1_redeemed_prize_1.code}",
        }
        request = self.factory.post("checar", user_redeemed_prize_mock_data)
        force_authenticate(request, user=self.user_partner_1)
        view = PartnerCheckRedeemPrizeViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.data["cpf"], self.user_1.cpf)

    # Testa um parceiro tentando verificar os detalhes de um prêmio usando um código inválido
    def test_partner_checking_user_prize_invalid_code(self):
        user_invalid_code = {
            "code": "123",
        }
        request = self.factory.post("checar", user_invalid_code)
        force_authenticate(request, user=self.user_partner_1)
        view = PartnerCheckRedeemPrizeViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    # Testa um parceiro tentando recuperar informações de um prêmio usando um código inválido
    def test_partner_retrieving_user_prize_invalid_code(self):
        user_invalid_code = {
            "code": "123",
        }
        request = self.factory.post("premios/usuarios/recuperar", user_invalid_code)
        force_authenticate(request, user=self.user_partner_1)
        view = PartnerRedeemPrizeViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    # Testa um parceiro recuperando informações de um prêmio resgatado por um usuário usando um código válido
    def test_partner_retrieving_user_prize(self):
        user_redeemed_prize_mock_data = {
            "code": f"{self.user_1_redeemed_prize_1.code}",
        }
        request = self.factory.post(
            "premios/usuarios/recuperar", user_redeemed_prize_mock_data
        )
        force_authenticate(request, user=self.user_partner_1)
        view = PartnerRedeemPrizeViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_message = "Prêmio utilizado com sucesso."
        self.assertIn(expected_message, str(response.data))

    # Testa a geração de um QR code para um prêmio resgatado por um usuário
    def test_partner_user_prize_get_qr_code(self):
        request = self.factory.get(f"premios/premio/qr-code/?prize={self.prize_1.pk}")
        force_authenticate(request, user=self.user_1)
        view = UserRedeemedPrizesQrCodeViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn(response.data[0]["qr_code"], self.user_1_redeemed_prize_1.qr_code)
