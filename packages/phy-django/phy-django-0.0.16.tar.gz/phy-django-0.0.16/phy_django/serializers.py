from rest_framework.serializers import *
from rest_framework.serializers import HyperlinkedModelSerializer as _HyperlinkedModelSerializer
from rest_framework.serializers import ModelSerializer as _ModelSerializer

__keep = (Serializer,)


class _PhyDjangoSerializerMixin(_ModelSerializer):
    class Meta:
        pass


class ModelSerializer(_PhyDjangoSerializerMixin, _ModelSerializer):
    pass


class HyperlinkedModelSerializer(_PhyDjangoSerializerMixin, _HyperlinkedModelSerializer):
    pass
