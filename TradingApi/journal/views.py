from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import response

from .models import Trade, Strategy
from .serializers import TradeSerializer,StrategySerializer

# Create your views here.

class StrategyViewSet(viewsets.ModelViewSet):
    queryset =Strategy.objects.all()
    serializer_class = StrategySerializer
    permission_classes =[IsAuthenticated]

class TradeViewSet(viewsets.ModelViewSet):
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)
    def perform_create(self):
        serializer.save(user=self.request.user)

    #wrapping my function with extra endpoint to get summary of trades, total number of trades and net profit/loss
    @action(detail=False, methods=['get'])
    def summary(self,request):
        trades = self.get_queryset()

        data = trades.aggregate(total_trades=Count('id'),Net_Profit=Sum('profit_loss'))
        return response(data, status=status.HTTP_200_OK)