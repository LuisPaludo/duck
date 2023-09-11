from rest_framework.serializers import ModelSerializer

from locations.models import Location, TouristAttraction


# Serializer Simples para a model Location
class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


# Serializer Simples para a model TouristAttraction
class TouristAttractionSerializer(ModelSerializer):
    class Meta:
        model = TouristAttraction
        fields = "__all__"