from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter

from .serializers import TouristAttractionSerializer, LocationSerializer
from locations.models import TouristAttraction, Location

# ViewSet Simples
# Todos podem observar quais os pontos turisticos da cidade, não necessitando autenticação
# Apenas o método get é permitido, implicando que apenas o administrador pode inserir um novo ponto turistico ("Mãe")
class LocationViewSet(ModelViewSet):
    permission_classes = (AllowAny,) 
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    http_method_names = ["get"]

# View Simples, permitindo apenas usuários autenticados
# Aqui apenas o método GET é permitido, ou seja, apenas o administrador pode adicionar novos pontos 
# Os pontos turisticos são recuperados através do campo code, que este será obtido através do QR Code lido
# Pelo usuário em um ponto turistico específico
class TouristAttractionViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TouristAttractionSerializer
    queryset = TouristAttraction.objects.all()
    http_method_names = ["get"]
    # Essa linha significa que esta viewset suporta filtragem de dados com base em certos campos.
    filter_backends = [SearchFilter,]
    # Define em qual campo da model será feita a pesquisa
    search_fields = ['code',]

