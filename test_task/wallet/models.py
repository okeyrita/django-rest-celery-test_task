from django.db import models, connection
from django.contrib.auth.models import User



class Wallets(models.Model):
    '''
    Model for representing a wallet item.
    '''
    user = models.OneToOneField(
        User, unique=True, related_name='wallets', on_delete=models.CASCADE)

    amount_rubles = models.FloatField(default=0.0)
    amount_euro = models.FloatField(default=0.0)
    amount_dollars = models.FloatField(default=0.0)

    def __str__(self):
        '''String for representing the Item object.'''
        return str(self.id)
