from django.db import models

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10, unique=True)
    quantity=models.IntegerField(default=1)
    buy_price= models.FloatField()

    def __str__(self):
        return self.name
