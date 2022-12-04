from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Card, Account

class TransactionSerializer(serializers.ModelSerializer):
    pass

class TrasactionTradeSerializer(TransactionSerializer):
    pass