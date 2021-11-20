from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import JsonResponse
from .serializer import *
from django.contrib.auth.hashers import check_password
from .models import *
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from django.db.models import Q
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
from rest_framework.permissions import IsAuthenticated

# Sellers Register API
class RegisterAPI(generics.CreateAPIView):
    queryset = Sellers.objects.all()
    serializer_class = SellerRegisterSerializer
# Buyerss Register API
class BuyerRegisterAPI(generics.CreateAPIView):
    queryset = Buyers.objects.all()
    serializer_class = BuyerRegisterSerializer

#Sellers login api
class SellerLoginView(APIView):
    def getToken(self):
        token = tokenGenerator()
        return token
    def post(self, request, format=None):
        try:
            token = self.getToken()
            access = token['access']
            refresh = token['refresh']
            emailaddress = request.data['username']
            password = request.data['password']
            record = Sellers.objects.filter(emailaddress=emailaddress).values(
                'id', 'emailaddress', 'firstname', 'lastname', 'stateofresidence').first()
            
                
            if record:
                passwordvalue = list(Sellers.objects.filter(
                    emailaddress= emailaddress).values_list('password', flat=True))
                if passwordvalue:    
                    b = passwordvalue[0]
                    passwordconfirm = check_password(password, b)
                    if passwordconfirm:
                        return JsonResponse({'data': record, 'token': access, 'status': True})
                    return JsonResponse({'status': False, 'message': 'Invalid password'})
                return JsonResponse({'status': False, 'message': 'Invalid username'})
            return JsonResponse({'status': False, 'message': 'Invalid user'})
            
            
        except Exception as e:
            return JsonResponse({'message': e, 'status': False})
# Buyers Login
class BuyerLoginView(APIView):
    def getToken(self):
        token = tokenGenerator()
        return token
    def post(self, request, format=None):
        try:
            token = self.getToken()
            access = token['access']
            refresh = token['refresh']
            emailaddress = request.data['username']
            password = request.data['password']
            buyer_record = Buyers.objects.filter(emailaddress=emailaddress).values(
                'id', 'emailaddress', 'firstname', 'lastname', 'location').first()
            if buyer_record:
                passwordvalue = list(Buyers.objects.filter(
                    emailaddress= emailaddress).values_list('password', flat=True))
                if passwordvalue:    
                    b = passwordvalue[0]
                    passwordconfirm = check_password(password, b)
                    if passwordconfirm:
                        return JsonResponse({'data': buyer_record, 'token': access, 'status': True})
                    return JsonResponse({'status': False, 'message': 'Invalid password'})
                return JsonResponse({'status': False, 'message': 'Invalid username'})
            return JsonResponse({'status': False, 'message': 'Invalid user'})
        except Exception as e:
            return JsonResponse({'message': e, 'status': False})
            

#sellers create products

class CreateProduct(generics.CreateAPIView):
    queryset = Products.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateProductSerializer

#sellers view their product
class SellersViewProduct(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None): 
        pk = request.query_params["id"]
        try:
            model = Products.objects.filter(sellersID__id = pk)
            serializer = ProductListSerializer(model, many = True)
            responseData = {'data': serializer.data, 'status': True}
        except Exception as e:
            responseData = {'message': str(e), 'status': False}
        return HttpResponse(json.dumps(responseData)) 

#sellers view product and interested buyers
class SellersViewProductBuyers(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None): 
        pk = request.query_params["id"]
        productrecords = list(
            Products.objects.filter(Q(salestatus = False), sellersID__id = pk).values('id', 'name', 'description', 'image', "price"))
        for interested_buyer in productrecords:
            interested_buyers = list(Orders.objects.filter(Q(productID__id = interested_buyer["id"]), orderstatus = "INTERESTED").values("buyersID__firstname", 
            "buyersID__emailaddress", "buyersID__location", "buyersID__lastname"))

            interested_buyer.update({'interestedbuyers': interested_buyers})
            interested_buyer["price"]= float(interested_buyer["price"])
            interested_buyer["image"]= f"{settings.CLOUDINARY_URL}/{interested_buyer['image']}"
            #interested_buyer["fullname"] = f"{interested_buyer['buyersID__firstname']} {interested_buyer['buyersID__firstname']}"
        responseData = {'data': productrecords, 'status': True}
        return HttpResponse(json.dumps(responseData), content_type="application/json")


#sellers SELL their product to one of the interested buyers
class SellersSellProduct(APIView):

    permission_classes = (IsAuthenticated,)

    def put(self, request, format=None): 
        pk = request.query_params["id"]
        buyer_id = request.query_params["buyerid"]
        try:
            model = Orders.objects.get(Q(productsID__id= pk), buyersID__id = buyer_id)
            product = Products.objects.get(id = pk)
            buyer = Buyers.objects.get(id = buyer_id)
            product_name = product.name
            buyers_name = f"{buyer.firstname} {buyer.lastname}"
            model.orderstatus= "SOLD"
            product.salestatus = True
            model.save(update_fields=['orderstatus'])
            product.save(update_fields=['salestatus'])
            responseData = {'message': f"{product_name} has been sold to {buyers_name}", 'status': True}
        except Exception as e:
            responseData = {'message': str(e), 'status': False}
        return HttpResponse(json.dumps(responseData))

#sellers delete a product
class SellerDeleteProduct(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, format=None):
        pk = request.query_params["id"]
        try:
            product = Products.objects.get(id= pk)
            product.delete()
            responseData = {"message": "Item deleted successfully!",'status': True}
        except useradmin.DoesNotExist:
            product = None
            responseData = {"message": "Item does not exist!",'status': False}
        return HttpResponse(json.dumps(responseData), content_type="application/json")

#buyers view product
class BuyersViewProduct(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        try:
            items_detail = []
            product = Products.objects.filter(salestatus = False).values("sellersID__id","price", "description", "image", "sellersID__stateofresidence")
            for items in product:
                sellersid = items["sellersID__id"]
                item_price = float(items["price"])
                items_description = items["description"]
                items_image = f"{settings.CLOUDINARY_URL}/{items['image']}"
                items_location = items["sellersID__stateofresidence"]
                item_detail = {"price":item_price, "items_description":items_description, "items_image":items_image,
                "seller_location":items_location, "sellersID": sellersid}
                items_detail.append(item_detail)
            responseData = {'data': items_detail, 'status': True}
        except Exception as e:
            responseData = {'message': str(e), 'status': True}
        return HttpResponse(json.dumps(responseData), content_type="application/json")

#buyers show interest in product
class BuyersChooseProduct(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        prod_id = request.query_params["id"]
        seller_id = list(Products.objects.filter(id = prod_id).values("sellersID__id"))[0]["sellersID__id"]
        buyer_id = request.query_params["buyerID"]
        orderstatus = "INTERESTED"
        data = {"orderstatus": orderstatus, "sellersID": seller_id, "buyersID":buyer_id, "productID":prod_id}
        data_interest = {"buyersID":buyer_id, "productID":prod_id}
        serializer = OrderSeializer(data = data)
        serializer_interest = InterestSeializer(data = data_interest)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Interest saved successfully"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer_interest.is_valid():
            serializer_interest.save()
        else:
            return Response(serializer_interest.errors, status=status.HTTP_400_BAD_REQUEST)





        


    




def tokenGenerator():
    headers = {'content-type': "application/json"}
    params = {"username": "seunmelody", "password": "melody"}
    url = settings.APP_URL
    print(url)
    fullurl = f"{url}/api/token/"
    r = requests.post(fullurl, data=params, verify=False)
    print(r)
    record = r.json()
    print(record)
    return record


