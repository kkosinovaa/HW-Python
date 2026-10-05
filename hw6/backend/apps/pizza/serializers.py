from rest_framework import serializers

from core.services.img_service import convert_to_jpeg

from apps.pizza.models import PizzaModel


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaModel
        fields = ('id','name','size','price','days','updated_at', 'created_at')

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return price
    def validate(self, attrs):
        price= attrs.get('price')
        size = attrs.get('size')
        if price==size:
            raise serializers.ValidationError('Price cannot be equal to size')
        return attrs

class PizzaPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaModel
        fields = ('photo',)

    def validate_photo(self, value):
            try:
                return convert_to_jpeg(value)
            except ValueError as error:
                raise serializers.ValidationError(str(error))
