from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


from locations.api.viewsets import LocationViewSet, TouristAttractionViewSet
from prize.api.viewsets import (
    PrizesViewSet,
    UserRedeemedPrizesViewSet,
    UserRedeemedPrizesQrCodeViewSet,
    PartnerCreatedPrizesViewSet,
    PrizeCategoryViewSet,
    PartnerRedeemPrizeViewSet,
    PartnerCheckRedeemPrizeViewSet,
)
from user_data.api.viewsets import HistoryViewSet, PartnerDetailsViewSet

router = routers.DefaultRouter()
router.register("locais", LocationViewSet)
router.register("pontos-turisticos", TouristAttractionViewSet)
router.register("premios", PrizesViewSet)
router.register("categorias", PrizeCategoryViewSet)
router.register("resgatar", UserRedeemedPrizesViewSet)
router.register("premios/criados", PartnerCreatedPrizesViewSet)
router.register("premios/premio/qr-code", UserRedeemedPrizesQrCodeViewSet)
router.register("usuario/historico", HistoryViewSet, basename="history")
router.register("parceiros/detalhes", PartnerDetailsViewSet, basename="partner-details")
router.register(
    "premios/usuarios/recuperar", PartnerRedeemPrizeViewSet, basename="recover"
)
router.register("checar", PartnerCheckRedeemPrizeViewSet, basename="check")


schema_view = get_schema_view(
    openapi.Info(
        title="DuckGO API",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "api/swagger.<slug:format>",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("accounts/", include("dj_rest_auth.urls")),
    path("accounts/registration/", include("dj_rest_auth.registration.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
