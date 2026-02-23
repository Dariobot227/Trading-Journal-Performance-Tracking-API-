from rest_framework import serializers
from .models import Trade, Strategy
from django.contrib.auth import get_user_model

User = get_user_model()

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = "__all__"
        read_only_fields= ['profit_loss','opened_at','closed_at']
    #making sure data we are getting is valid and wont break the business logic
    def validate_price_inputs(self,data):
        if data['stop_loss'] >= data['entry_price'] and data['direction'] == 'BUY':
            raise serializers.ValidationError("Stop loss must be below entry price for BUY trades")
        if data ['stop_loss'] <= data['entry_price'] and data['direction'] == 'SELL':
            raise serializers.ValidationError("stop loss must be above Entry for Sell trades")
        return data
        #mkaing sure lot size is always positive
    def validate_lot_size(self, value):
        if value <=0:
            raise serializers.ValidationError("lot_size cant be negetive")
        return value

    def validate_pair(self,value):
        value= value.upper()
        if value is not Trades.CONTRACT_SIZES:
            raise serializers.ValidationError("Unsupported Trading pair")
        return value

    def validate(self,data):
        if data.get("status")=="CLOSED" and not data.get("exit_price"):
            raise serializers.ValidationError("Exit price must be provided when closing the trade")
            return data
  
class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = "__all__"
        
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user 



