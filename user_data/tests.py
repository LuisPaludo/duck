from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import force_authenticate
from model_bakery import baker

from .models import CustomUser, History

from .api.viewsets import (
    HistoryViewSet,
    CustomVerifyEmailView,
    PartnerDetailsViewSet,
)

class TestUserData(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_1 = baker.make(CustomUser)
        