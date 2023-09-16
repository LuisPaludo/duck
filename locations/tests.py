from asyncio.windows_events import NULL
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
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
        self.location_1 = baker.make(Location, name = "Lugar 01")
        self.location_2 = baker.make(Location, name = "Lugar 02")
        self.tourist_attraction_1 = baker.make(TouristAttraction)

    def _get_request(self,pk=None):
        if pk:
            request = self.factory.get(f'/locais/{pk}')
            view = LocationViewSet.as_view({'get': 'retrieve'})
            return view(request, pk=pk)
        else:
            request = self.factory.get('locais')
            view = LocationViewSet.as_view({'get': 'list'})
            return view(request)
        
    def test_list_location(self):
        response = self._get_request()
        self.assertEqual(response.status_code, HTTP_200_OK)
    
    def test_retrieve_location(self):
        response = self._get_request(pk = self.location_1.pk)
        self.assertEqual(response.status_code, HTTP_200_OK)

class TouristAttractionTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = baker.make(CustomUser)
        self.location_1 = baker.make(Location, name = "Lugar 01")
        self.location_2 = baker.make(Location, name = "Lugar 02")
        self.tourist_attraction_1 = baker.make(TouristAttraction)

    def _get_request_auth(self,code=None):
        if code:
            request = self.factory.get(f'/pontos-turisticos/?search={code}')
            force_authenticate(request, user=self.user)
            view = TouristAttractionViewSet.as_view({'get': 'list'})
            return view(request)
        else:
            request = self.factory.get('pontos-turisticos')
            force_authenticate(request, user=self.user)
            view = TouristAttractionViewSet.as_view({'get': 'list'})
            return view(request)
        
    def _get_request_without_auth(self,code=None):
        if code:
            request = self.factory.get(f'/pontos-turisticos/?search={code}')
            view = TouristAttractionViewSet.as_view({'get': 'list'})
            return view(request)
        else:
            request = self.factory.get('pontos-turisticos')
            view = TouristAttractionViewSet.as_view({'get': 'list'})
            return view(request)
        
    def test_list_tourist_attraction(self):
        response = self._get_request_auth()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, [])
    
    def test_retrieve_tourist_attraction_with_code(self):
        response = self._get_request_auth(code = self.tourist_attraction_1.code)
        first_item = response.data[0]
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(first_item['name'], self.tourist_attraction_1.name)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_tourist_attraction_with_code_without_auth(self):
        response = self._get_request_without_auth(code = self.tourist_attraction_1.code)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)