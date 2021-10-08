from rest_framework import serializers

from django.contrib.auth.models import User
from started_app.models import Shoe, Brand, Material


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'description', 'country']


class ShoeSerializer(serializers.HyperlinkedModelSerializer):
    material = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Material.objects.all()
    )

    class Meta:
        model = Shoe
        fields = ['id', 'name', 'price', 'material', 'brand']

    brand = BrandSerializer(required=False)

    def create(self, validated_data):
        print(validated_data)
        brand_data = validated_data.pop('brand')
        brand = Brand.objects.create(**brand_data)
        shoe = Shoe.objects.create(**validated_data, brand=brand)
        return shoe
