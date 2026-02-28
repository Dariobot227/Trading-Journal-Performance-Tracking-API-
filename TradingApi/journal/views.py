from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

from .models import Trade, Strategy, Profile
from .serializers import TradeSerializer,StrategySerializer,RegisterSerializer, ProfileSerializer

from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
User = get_user_model()

class Homepage(View):
    def get(self, request):
        return render(request, 'index.html')


class StrategyViewSet(viewsets.ModelViewSet):
    queryset =Strategy.objects.all()
    serializer_class = StrategySerializer
    permission_classes =[IsAuthenticated]
    def get_queryset(self):
        return Strategy.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TradeViewSet(viewsets.ModelViewSet):
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        strategy = serializer.validated_data.get("strategy")

        if strategy and strategy.user != self.request.user:
            raise PermissionDenied("You cannot use another user's strategy")

        serializer.save(user=self.request.user)


    #wrapping my function with extra endpoint to get summary of trades, total number of trades and net profit/loss
    @action(detail=False, methods=['get'])
    def summary(self,request):
        trades = self.get_queryset()

        data = trades.aggregate(total_trades=Count('id'),Net_Profit=Sum('profit_loss'))
        return Response(data, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # allow anyone to register
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "User registered successfully",
            "token": token.key
        })
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Profile.objects.all()
        return Profile.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)