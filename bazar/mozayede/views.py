from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Provider , Customer , Auction
from rest_framework.permissions import IsAuthenticated
from .permission import IsCustomer , IsProvider
from rest_framework.exceptions import ValidationError
from .serializers import AuctionSerializer , CustomerOfferSerializer
from django.utils import timezone
from datetime import timedelta
<<<<<<< HEAD
import datetime
=======
from datetime import datetime, time
>>>>>>> fda8e4fd7acb61dd1f1994a8b73c30235f9f0890


class Login(TokenObtainPairView):
    pass
class NewAuction(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsProvider , IsAuthenticated]
        elif self.request.method == "GET":
            self.permission_classes = [IsCustomer , IsAuthenticated]
        return super(NewAuction, self).get_permissions()
    
    def perform_create(self, serializer):
        my_user = self.request.user
        my_provider = Provider.objects.get(user = my_user)
        return serializer.save(Provider = my_provider )
    
    
class AddOffer(generics.UpdateAPIView):
    
    queryset = Auction.objects.all()
    serializer_class = CustomerOfferSerializer
    permission_classes = [IsCustomer , IsAuthenticated]

    def perform_update(self, serializer):
        my_auction = serializer.instance
        given_price = self.request.data.get('price')
        if given_price < my_auction.current_price + 200:
            raise ValidationError("price must be bigger")
        my_user = self.request.user
        my_customer = Customer.objects.get(user = my_user)
        my_auction.last_customer = my_customer
        my_auction.current_price = given_price
        end_datetime = datetime.combine(datetime.today(), my_auction.end_date)
        new_end_datetime = end_datetime + timedelta(minutes=10)

        # Update only the time part
        my_auction.end_date = new_end_datetime.time()

        super().perform_update(serializer)