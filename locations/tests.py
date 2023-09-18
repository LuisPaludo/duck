from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import force_authenticate
from model_bakery import baker

from .models import Location, TouristAttraction
from user_data.models import CustomUser

from .api.viewsets import LocationViewSet, TouristAttractionViewSet

# Create your tests here.

class LocationTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = baker.make(CustomUser)
        self.location_1 = baker.make(Location, name="Lugar 01")
        self.location_2 = baker.make(Location, name="Lugar 02")
        self.tourist_attraction_1 = baker.make(TouristAttraction)

    # Retorna a resposta para a requisição GET
    def _get_request(self, pk=None):
        if pk:
            request = self.factory.get(f"/locais/{pk}")
            view = LocationViewSet.as_view({"get": "retrieve"})
            return view(request, pk=pk)
        else:
            request = self.factory.get("locais")
            view = LocationViewSet.as_view({"get": "list"})
            return view(request)

    # Testa a listagem de locais
    def test_list_location(self):
        response = self._get_request()
        self.assertEqual(response.status_code, HTTP_200_OK)

    # Testa a recuperação de detalhes de um local específico pelo seu ID
    def test_retrieve_location(self):
        response = self._get_request(pk=self.location_1.pk)
        self.assertEqual(response.status_code, HTTP_200_OK)


class TouristAttractionTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = baker.make(CustomUser)
        self.location_1 = baker.make(Location, name="Lugar 01")
        self.location_2 = baker.make(Location, name="Lugar 02")
        self.tourist_attraction_1 = baker.make(TouristAttraction)

    # Retorna a resposta para a requisição GET com autenticação
    def _get_request_auth(self, code=None):
        if code:
            request = self.factory.get(f"/pontos-turisticos/?search={code}")
            force_authenticate(request, user=self.user)
            view = TouristAttractionViewSet.as_view({"get": "list"})
            return view(request)
        else:
            request = self.factory.get("pontos-turisticos")
            force_authenticate(request, user=self.user)
            view = TouristAttractionViewSet.as_view({"get": "list"})
            return view(request)

    # Retorna a resposta para a requisição GET sem autenticação
    def _get_request_without_auth(self, code=None):
        if code:
            request = self.factory.get(f"/pontos-turisticos/?search={code}")
            view = TouristAttractionViewSet.as_view({"get": "list"})
            return view(request)
        else:
            request = self.factory.get("pontos-turisticos")
            view = TouristAttractionViewSet.as_view({"get": "list"})
            return view(request)

    # Testa a listagem de pontos turísticos com autenticação
    def test_list_tourist_attraction(self):
        response = self._get_request_auth()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, [])

    # Testa a recuperação de um ponto turístico específico pelo seu código com autenticação
    def test_retrieve_tourist_attraction_with_code(self):
        response = self._get_request_auth(code=self.tourist_attraction_1.code)
        first_item = response.data[0]
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(first_item["name"], self.tourist_attraction_1.name)
        self.assertEqual(len(response.data), 1)

    # Testa a recuperação de um ponto turístico específico pelo seu código sem autenticação
    def test_retrieve_tourist_attraction_with_code_without_auth(self):
        response = self._get_request_without_auth(code=self.tourist_attraction_1.code)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
