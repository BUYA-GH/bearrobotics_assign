from django.db import models
from django.contrib.auth.hashers import make_password

class Card(models.Model):
    cardNum = models.CharField(max_length=16, unique=True)
    pinNum = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.cardNum}"

# Create your models here.
class Account(models.Model):
    accountNumber = models.CharField(max_length=255, unique=True)
    balance = models.IntegerField(default=0)

    author = models.OneToOneField(Card, on_delete=models.CASCADE, related_name="card_account")

    def __str__(self):
        return f"{self.accountNumber} / {self.author}"

class Transition(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_transition")
    receivedPaid = models.IntegerField()

    transact_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.account} - {self.transact_at}"