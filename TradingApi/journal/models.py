from django.db import models
from django.core.exceptions import ValidationError#for validation errors that may occur
# Create your models here.

class Trade(models.Model):
    DIRECTION_CHOICES = [
        ('BUY'), 
        ('SELL'),]

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

    pair = models.CharField(max_length=20)

    lot_size = models.DecimalField(max_digits=5,decimal_places=2)
    direction = models.CharField(max_length=4, choices=DIRECTION_CHOICES)
    entry_price = models.DecimalField(max_digits=20, decimal_places=10)
    exit_price = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True) #actual exit level, can differ from planned take_profit or stop_loss

    take_profit = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True) #planned exit level
    stop_loss = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True) #risk control level
    profit_loss = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True) #calculated when exit_price is set

    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    emotion = models.CharField(max_length=255,choices=EMOTION_CHOICES)
    #function to get contract size based on pair
    def get_contract_size(self):
        return self.CONTRACT_SIZES.get(self.pair, 100000) #default to 100k if pair not found

    #FUNC to automatically calculate profit/loss when exit_price is set
    def calculate_profit_loss(self):
        if self.exit_price is None:
            return 0
   
        if self.direction == 'BUY':
            return (self.exit_price -self.entry_price)*self.lot_size*self.get_contract_size()
        else: #SELL
            return (self.entry_price - self.exit_price)*self.lot_size*self.get_contract_size()
        return 0
    # the formulae are well explained in the readme.md file of the project.
    

    #validation to ensure the pair is supported
    def validate_pair(self):
        if self.pair.upper() not in self.CONTRACT_SIZES:
            raise ValidationError("This trading pair is unsupported")
    #normalisation for uniformity

    def save(self, *args, **kwargs):
         if self.pair:
            self.pair = self.pair.upper()
        #validation, is the pair in the ones suported

    self.validate_pair()

    if self.exit_price:
        self.profit_loss = self.calculate_profit_loss()

    super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.direction} {self.lot_size} lots of {self.pair} at {self.entry_price}"

class Strategy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name
class TraderProfile(models.Model):
    username = models.CharField(max_length=100)
    
