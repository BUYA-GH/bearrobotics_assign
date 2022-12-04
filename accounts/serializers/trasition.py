from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Card, Account, Transition

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = ('account', 'balance', 'author',)
        read_only_fields = ('account', 'balance', 'author',)

class TrasactionWorkSerializer(TransactionSerializer):
    