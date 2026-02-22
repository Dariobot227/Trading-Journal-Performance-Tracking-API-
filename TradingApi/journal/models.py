from django.db import models
from django.core.exceptions import ValidationError#for validation errors that may occur
from django.contrib.auth.models  import User

# Create your models here.
class Strategy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name="trades")
    Account_size = models.DecimalField(max_digits=20, decimal_places=2)
    current_balance = models.DecimalField(max_digits=20, decimal_places=2)

    def update_balance(self, profit_loss):
        self.current_balance += profit_loss
        self.save()

class Trade(models.Model):
    DIRECTION_CHOICES = [
        ("BUY", "Buy"), 
        ("SELL", "Sell"),] #value then display_name, lerant that the hard way

    CONTRACT_SIZES = {
        "XAUUSD":100,
        "XAGUSD":5000,
        "EURUSD":100000,
        "GBPUSD":100000,
        "USDJPY":100000,
        "BTCUSD":1,
    }

    EMOTION_CHOICES = [
        ('GREED', 'Greed'),
        ('FEAR', 'Fear'),
        ('HOPE', 'Hope'),
        ('FOMO', 'FOMO'),
        ('CONFIDENCE', 'Confidence'),
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trades")
    pair = models.CharField(max_length=20)
    strategy = models.ForeignKey(Strategy, on_delete=models.SET_NULL, null=True)

    lot_size = models.DecimalField(max_digits=5,decimal_places=2)
    direction = models.CharField(max_length=4, choices=DIRECTION_CHOICES)
    entry_price = models.DecimalField(max_digits=20, decimal_places=10)
    exit_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True) #actual exit level, can differ from planned take_profit or stop_loss

    take_profit = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True) #planned exit level
    stop_loss = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True) #risk control level
    profit_loss = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True) #calculated when exit_price is set

    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default="OPEN")
    emotion = models.CharField(max_length=255,choices=EMOTION_CHOICES)
    #function to get contract size based on pair
    def get_contract_size(self):
        return self.CONTRACT_SIZES.get(self.pair.upper(), 100000) #default to 100k if pair not found

    #FUNC to automatically calculate profit/loss when exit_price is set
    def calculate_profit_loss(self):
        if not self.exit_price:
            return 0
        price_diff = self.exit_price - self.entry_price
        if self.direction == "SELL":
            price_diff = -price_diff
        return price_diff * self.lot_size * self.get_contract_size()

    #validation, everything uppercase, Normalization concept
    def validate_pair(self):
        if self.pair.upper() not in self.CONTRACT_SIZES:
            raise ValidationError("unsupported trading pair")

    def validate_lot_size(self):
        if self.lot_size <= 0:
            raise ValidationError("lot size must be positive")

    def save(self, *args, **kwargs):
        if self.pair:
            self.pair = self.pair.upper() #normalize to uppercase
        self.validate_pair() #validate pair before saving
        if self.exit_price and self.status == "CLOSED":
            self.profit_loss = self.calculate_profit_loss() 
            
            try:
                Profile = self.user.Profile
                
                if not Trade.objects.filter(id=self.id, status="CLOSED").exists():
                    profile.update_balance(self.profit_loss)
            except Exception:
                pass
            super().save(*args, **kwargs)
        def __str__(self):
            return f"{self.direction} {self.lot_size} lots of {self.pair}"