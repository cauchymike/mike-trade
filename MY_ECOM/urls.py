"""MY_ECOM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from eccomerce.views import *
from eccomerce.serializer import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/registerbuyer/', BuyerRegisterAPI.as_view(), name='register_buyer'),
    re_path(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^api/token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
    path('api/login/', SellerLoginView.as_view(), name='login'),
    path('api/loginbuyer/', BuyerLoginView.as_view(), name='login_buyer'),
    path('api/createproduct/', CreateProduct.as_view(), name='createproduct'),
    path('api/viewproduct/', SellersViewProduct.as_view(), name='viewproduct'),
    path('api/viewproductbuyers/', SellersViewProductBuyers.as_view(), name='viewproductbuyers'),
    path('api/sellproduct/', SellersSellProduct.as_view(), name='sell_product'),
    path('api/buyersviewproduct/', BuyersViewProduct.as_view(), name='viewproduct_buyer'),
    path('api/buyerschooseproduct/', BuyersChooseProduct.as_view(), name='chooseproduct_buyer'),
    path('api/deleteproduct/', SellerDeleteProduct.as_view(), name='viewproduct'),

]
