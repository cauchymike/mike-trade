from django.contrib.auth.hashers import make_password
from django.http.request import validate_host
from django.contrib.auth.hashers import make_password
from .models import *
from rest_framework import generics, permissions, serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.validators import UniqueValidator



# Registeration Serializer
class SellerRegisterSerializer(serializers.ModelSerializer):

    emailaddress = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Sellers.objects.all())]
            )
    class Meta:
        model = Sellers
        fields = ('id', 'firstname','lastname','emailaddress', 'password', "stateofresidence")
        extra_kwargs = {'password': {'write_only': True, 'required': True},
        'emailaddress':{'required': True},
        'firstname':{'required': True}, 'lastname':{'required': True}}
    def create(self, validated_data):
        seller = Sellers.objects.create(emailaddress= validated_data['emailaddress'],
        firstname = validated_data['firstname'],lastname = validated_data['lastname'],
        password =  make_password(
                    validated_data['password'], salt=None, hasher='default'),
        stateofresidence = validated_data["stateofresidence"])

        seller.save()
        return seller

# Buyers Registeration Serializer
class BuyerRegisterSerializer(serializers.ModelSerializer):

    emailaddress = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Buyers.objects.all())]
            )
    class Meta:
        model = Buyers
        fields = ('id', 'firstname','lastname','emailaddress', 'password', "location")
        extra_kwargs = {'password': {'write_only': True, 'required': True},
        'emailaddress':{'required': True},
        'firstname':{'required': True}, 'lastname':{'required': True}}

    def create(self, validated_data):
        buyer = Buyers.objects.create(emailaddress= validated_data['emailaddress'],
        firstname = validated_data['firstname'],lastname = validated_data['lastname'],
        password =  make_password(
                    validated_data['password'], salt=None, hasher='default'),
        location = validated_data["location"])

        buyer.save()
        return buyer

#Seller Serializer
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sellers
        fields = ('id', 'firstname', 'emailaddress', 'lastname', 'stateofresidence')

#Product Serializer
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'name', 'description', 'price')

#create product serializer
class CreateProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Products
        fields = ('sellersID', 'name', 'description', 'price', 'image')
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
            'price': {'required': True},
        }
    def create(self, validated_data):
        product = Products.objects.create(price= validated_data['price'],
        name = validated_data['name'],description = validated_data['description'],
        image = validated_data["image"], sellersID = validated_data["sellersID"])
        product.save()
        return product

#list of product serializer

class ProductListSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    #total_amount = SerializerMethodField()
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Products
        fields = "__all__"

class OrderSeializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Orders
        fields = "__all__"

class InterestSeializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = BuyersInterest
        fields = "__all__"

